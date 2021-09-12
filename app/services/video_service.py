from app.utils.timelapse import run_timelapse
from app.utils.stabilization import run_stabilization
from app.services.process_service import get_all_process_types, get_processes_by_type, run_process, complete_process
# from multiprocessing import Pool
import time

NUMBER_OF_WORKERS = 3


def timelapse_runner(vid_obj):
    run_process(vid_obj["id"])
    run_timelapse(vid_obj["filename"])
    complete_process(vid_obj["id"])


def stabilization_runner(vid_obj):
    run_process(vid_obj["id"])
    run_stabilization(vid_obj["filename"])
    complete_process(vid_obj["id"])


def process_video():
    while True:
        process_types = get_all_process_types()
        for process_type in process_types:
            processes = get_processes_by_type(process_type["id"])
            vid_objs = map(
                lambda p: {"id": p["id"], "filename": p["hashed_name"] + "-" + p["filename"]}, processes)
            runner = eval(process_type["name"] + "_runner")
            # with Pool(NUMBER_OF_WORKERS) as p:
            #     p.map(runner, vid_objs)
            for vid_obj in vid_objs:
                runner(vid_obj)
        time.sleep(60)