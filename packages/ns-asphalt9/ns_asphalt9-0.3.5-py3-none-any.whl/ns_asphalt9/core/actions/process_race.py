import os
import threading
import uuid
from queue import LifoQueue, Queue

from .. import consts, globals, ocr, screenshot
from ..controller import Buttons, pro
from ..utils.log import logger
from ..utils.track_navi_data import get_navi_data
from .common import get_race_mode


def generate_random_filename():
    random_name = str(uuid.uuid4().hex)[:8]
    return random_name


def get_action(progress, navi_data):
    real_progress = progress + 2
    for p, v in navi_data:
        if p - real_progress <= 4 and p - real_progress > 0:
            if p - real_progress < 2:
                return [v]
            if p - real_progress < 3:
                return [v] * 2
            if p - real_progress <= 4:
                return [v] * 3
    else:
        return ["Y"] * 2


def race_worker(queue, navi_data, pro, race_navi_event):
    while race_navi_event.is_set():
        ret = queue.get()
        if isinstance(ret, int):
            action = get_action(ret, navi_data)
            pro.press_group(action, 0)
        if isinstance(ret, str) and ret == "stop":
            break
    logger.info("Action woker quit.")


def thread_exec_command(cmd):
    def exec_command(cmd):
        os.system(cmd)

    t = threading.Thread(target=exec_command, args=(cmd,), daemon=True)
    t.start()


def screenshot_worker(queue, race_navi_event):
    while race_navi_event.is_set():
        image_path = f"/tmp/a9_{generate_random_filename()}.jpg"
        screenshot.screenshot(image_path)
        queue.put(image_path)


def start_race_worker(queue, navi_data, pro, race_navi_event):
    t = threading.Thread(
        target=race_worker, args=(queue, navi_data, pro, race_navi_event), daemon=True
    )
    t.start()
    return t


def start_screenshot_worker(queue, race_navi_event):
    t = threading.Thread(
        target=screenshot_worker, args=(queue, race_navi_event), daemon=True
    )
    t.start()
    return t


class ProgessManager:
    def __init__(self) -> None:
        self.history_progress = []

    def get_progress(self, progress):
        msg = f"real progress = {progress}"
        if not self.history_progress and progress < 0:
            return progress
        fit_progress = self.get_fit_progress()
        if fit_progress:
            if progress < 0 or progress > 100:
                progress = fit_progress
            elif progress < self.history_progress[-1]:
                progress = fit_progress
            elif (
                progress - self.history_progress[-1] > 10
                and progress - fit_progress > 5
            ):
                progress = fit_progress
            else:
                pass
        if 0 < progress < 100:
            self.history_progress.append(progress)
        logger.info(f"{msg} fit_progress = {fit_progress} final_progress = {progress}")
        return progress

    def get_fit_progress(self):
        if len(self.history_progress) >= 2:
            y = self.history_progress
            x = [i for i in range(0, len(y))]
            # 计算拟合的斜率和截距
            n = len(x)
            mean_x = sum(x) / n
            mean_y = sum(y) / n
            m = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y)) / sum(
                (xi - mean_x) ** 2 for xi in x
            )
            b = mean_y - m * mean_x
            fit_progress = int(n * m + b)
            return fit_progress


def process_race():
    logger.info("Start racing.")
    track = None
    progress = None
    queue = Queue()
    image_queue = LifoQueue()
    race_navi_event = threading.Event()
    mode = get_race_mode()
    enable_navi = globals.CONFIG[mode]["自动选路"]
    logger.info(f"enable_navi = {enable_navi}")
    for i in range(60):
        page = ocr.OCR.get_page()
        if page.name == consts.loading_race:
            track = ocr.OCR.get_track()
            if track:
                logger.info(f"Current track is {track['trackcn']}")
            navi_data = get_navi_data(track["tracken"]) if track else None
            if navi_data and enable_navi:
                logger.info("Start aciton worker")
                race_navi_event.set()
                start_race_worker(queue, navi_data, pro, race_navi_event)
                start_screenshot_worker(image_queue, race_navi_event)
                break

        if ocr.OCR.has_next() or page.name in [
            consts.race_score,
            consts.race_results,
            consts.race_reward,
            consts.system_error,
            consts.connect_error,
            consts.no_connection,
            consts.multi_player,
        ]:
            break

        pro.press_button(Buttons.Y, 0.7)
        pro.press_button(Buttons.Y, 0)

    if race_navi_event.is_set():
        progress_manager = ProgessManager()
        for i in range(60):
            image_path = image_queue.get()
            progress = ocr.OCR.get_progress(image_path)
            logger.info(f"Current progress is {progress}")
            thread_exec_command(f"cp {image_path} output.jpg")
            if progress < 0 and ocr.OCR.has_next(image_path):
                queue.put("stop")
                race_navi_event.clear()
                break
            else:
                progress = progress_manager.get_progress(progress)
                queue.put(progress)
        else:
            queue.put("stop")
    thread_exec_command("sudo rm /tmp/a9_*.jpg")
    globals.FINISHED_COUNT += 1
    logger.info(f"Already finished {globals.FINISHED_COUNT} times loop count = {i}.")
