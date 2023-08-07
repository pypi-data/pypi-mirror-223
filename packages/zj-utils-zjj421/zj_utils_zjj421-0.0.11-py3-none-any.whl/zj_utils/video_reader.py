#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: zhangjian
# date: 2023/7/13
import _queue
import logging
from queue import Queue
from threading import Thread

import cv2

from .helper import get_time_str, setup_logger
from .timer import MyTimer, FPSRealTime

__all__ = ['FrameInfo', 'VideoStreamReader', 'read_video_demo']


class FrameInfo(object):
    def __init__(self, image, frame_idx=None, frame_elapsed_ms=None):
        self.image = image
        self.frame_idx = frame_idx
        self.frame_elapsed_ms = frame_elapsed_ms
        self.process_ret = None

    def get_image(self):
        return self.image

    def set_image(self, image):
        self.image = image

    def get_frame_idx(self):
        return self.frame_idx

    def get_frame_elapsed_s(self):
        return self.frame_elapsed_ms / 1000

    def get_frame_elapsed_ms(self):
        return self.frame_elapsed_ms

    def set_ret(self, result):
        self.process_ret = result

    def get_ret(self):
        return self.process_ret


class VideoStreamReader(object):
    def __init__(self, video_input_param):
        self.video_input_param = video_input_param
        self.stopped = False
        self.mylogger = logging.getLogger('demo')
        self.mylogger.info('VideoStreamReader init done.')

    def load_camera(self, ):
        cap = cv2.VideoCapture(self.video_input_param)
        self.mylogger.info(
            f'Video is {"opened." if cap.isOpened() else "not opened."}')
        cap_fps = cap.get(5)
        height, width = cap.get(cv2.CAP_PROP_FRAME_HEIGHT), cap.get(
            cv2.CAP_PROP_FRAME_WIDTH)
        self.mylogger.info(
            f'Video stream FPS: {cap_fps}\tshape: ({height}, {width})')
        self.mylogger.info(
            f'Load video stream from {self.video_input_param} done.')
        return cap

    def run(self, queue_i):
        self.mylogger.info('VideoStreamReader running ...')
        cap = self.load_camera()
        frame_idx = 0
        mytimer = MyTimer()

        while not self.stopped:
            mytimer.restart()
            ret = cap.grab()
            frame_idx += 1
            if not ret:
                self.mylogger.info(
                    f'---VideoStreamReader--- Grab NONE FRAME, Cap is opened: {cap.isOpened()}'
                )
                cap = self.load_camera()
            if queue_i.full():
                continue
            else:
                ret, image = cap.retrieve()
            self.mylogger.debug(
                f'---VideoStreamReader--- cap read elapsed: {mytimer.elapsed():.2f}ms'
            )
            if ret:
                frame = FrameInfo(image=image,
                                  frame_idx=frame_idx,
                                  frame_elapsed_ms=cap.get(
                                      cv2.CAP_PROP_POS_MSEC))
                queue_i.put(frame)
                self.mylogger.debug(
                    f'---VideoStreamReader--- Put Frame-{frame_idx} to the list ---- len:{queue_i.qsize()} '
                    f'elapsed: {mytimer.elapsed():.2f}ms')
            else:
                self.mylogger.info(
                    f'---VideoStreamReader--- READ NONE FRAME, Cap is opened: {cap.isOpened()}'
                )
                cap = self.load_camera()

        cap.release()
        self.mylogger.info('Camera is closed.')

    def stop(self):
        self.stopped = True


def onMouse(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(f'({x}, {y})')


def show_video(queue_i, video_name="Video", window_size=(540, 960)):
    cv2.namedWindow(video_name, 0)  # 0可调大小，注意：窗口名必须imshow里面的一窗口>名一直
    cv2.resizeWindow(video_name, window_size[1], window_size[0])  # 设置宽和高
    fps_obj = FPSRealTime(buffer_len=250)
    while True:
        try:
            frame = queue_i.get(timeout=5)
        except _queue.Empty:
            print(f'no frame, exit.')
            exit()
        image = frame.get_image()
        fps = fps_obj.get_fps(number=1)
        cv2.putText(image, f'FPS: {fps}', (40, 40), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 4)
        cv2.imshow(video_name, image)
        cv2.setMouseCallback(video_name, onMouse)
        # Process Key (ESC: end) #################################################
        # key = cv2.waitKey(10)
        # if key == 27:  # ESC
        #     break
        if cv2.waitKey(10) & 0xFF == ord('q'):
            print(f'user exit.')
            break


def read_video_demo(video_url):
    timer_str = get_time_str()
    log_root = f'logs/{timer_str[:10]}'
    setup_logger('demo', log_root=log_root, log_file_save_basename=f'{timer_str}.log', level='INFO', screen=True,
                 tofile=False, msecs=True)
    video_reader = VideoStreamReader(video_url)
    queue_i = Queue(maxsize=1)
    video_reader_worker = Thread(target=video_reader.run, kwargs={"queue_i": queue_i}, daemon=True)
    video_reader_worker.start()
    show_video(queue_i)


def main():
    video_url = ''
    read_video_demo(video_url)


if __name__ == '__main__':
    main()
