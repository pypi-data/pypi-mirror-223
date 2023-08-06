# -*- coding: utf-8 -*-
"""
@Time : 2023/6/22 10:14
@Author : sdb20200101@gmail.com
@File: imageView.py
@Software : PyCharm
"""
import math

import numpy as np
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *
from .constant import ROI
from .RectangleRoi import RectangleRoi
from .CircleRoi import CircleRoi
from .LineRoi import LineRoi
from .AngleRoi import AngleRoi
from .EllipseRoi import EllipseRoi


class ImageViewer(QGraphicsView):

    def __init__(self, cursor: QLineEdit, roi: ROI, parent: QWidget):
        super().__init__()
        self.cursor = cursor
        self.roi_state = roi
        self.parent = parent

        # 设置视图参数

        self.setRenderHint(QPainter.RenderHint.Antialiasing, True)  # 图片抗锯齿
        self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        # self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        # self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        # 创建场景并添加到视图
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)

        # 添加图像项并居中显示
        self.pixmap_item = QGraphicsPixmapItem()
        self.scene.addItem(self.pixmap_item)
        self.centerOn(self.pixmap_item)
        self.pixmap_item.setCursor(Qt.CursorShape.ArrowCursor)

        # 设置初始状态
        self.image = None
        self.roi = None
        self.roi_select_status = False
        self.handle_move_status = False
        self.roi_move_status = False
        self.start_pos = None
        self.init_point = None
        self.handle_index = None
        self.mouseMoveEvent = self.mouseMoveEventNoRoi
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.initScale = None
        self.points = []
        self.pressed_keys = []

    def clear(self):
        self.roi = None
        self.roi_select_status = None
        self.handle_move_status = None
        self.roi_move_status = None
        self.start_pos = None
        self.init_point = None
        self.handle_index = None
        self.points = []
        self.pressed_keys = []
        for item in self.scene.items():
            if not isinstance(item, QGraphicsPixmapItem):
                self.scene.removeItem(item)

    def setImage(self, image):
        # 设置图像
        self.image = image
        pixmap = QPixmap.fromImage(self.image)
        self.pixmap_item.setPixmap(pixmap)
        self.scene.setSceneRect(pixmap.rect())
        self.fitInView(self.scene.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)
        self.initScale = self.transform().m11()
        self.clear()

    def setImageNoQImage(self, img):
        img = np.ascontiguousarray(img)
        height, width = img.shape
        img1 = QImage(img, width, height, width, QImage.Format.Format_Grayscale8)
        self.setImage(img1)

    def setPixmap(self, pix: QPixmap):
        self.image = pix.toImage()
        self.pixmap_item.setPixmap(pix)
        self.scene.setSceneRect(pix.rect())
        self.fitInView(self.scene.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)
        self.initScale = self.transform().m11()
        self.clear()

    def wheelEvent(self, event):
        # 实现缩放
        if self.image is None:
            return
        mouse_point = self.mapToScene(event.position().toPoint())
        width = self.viewport().width()
        height = self.viewport().height()

        hScale = event.position().x() / width
        vScale = event.position().y() / height

        scaleFactor = self.transform().m11()
        factor = 1.2 if event.angleDelta().y() > 0 else 0.8

        if scaleFactor >= self.initScale or factor == 1.2:
            self.scale(factor, factor)

        viewPoint = self.transform().map(mouse_point)

        self.horizontalScrollBar().setValue(int(viewPoint.x() - width * hScale))
        self.verticalScrollBar().setValue(int(viewPoint.y() - height * vScale))

        if self.roi is not None:
            scaleFactor = self.transform().m11()
            self.roi.scale_factor = scaleFactor

    def mousePressEventNoRoi(self, event: QMouseEvent):
        super().mousePressEvent(event)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def mouseReleaseEventNoRoi(self, event: QMouseEvent):
        super().mouseReleaseEvent(event)
        self.setCursor(Qt.CursorShape.ArrowCursor)

    def mouseMoveEventNoRoi(self, event):
        # 实时更新鼠标位置和 RGB 值
        if self.image is None:
            return

        pos = self.mapToScene(event.pos())
        self.pixmap_item.setCursor(Qt.CursorShape.ArrowCursor)
        x = int(pos.x())
        y = int(pos.y())

        if 0 <= x < self.image.width() and 0 <= y < self.image.height():
            color = QColor(self.image.pixel(x, y))
            r = color.red()
            g = color.green()
            b = color.blue()
            self.cursor.setText(f'[{x},{y}] [{r},{g},{b}]')
        else:
            self.cursor.setText('')

        super().mouseMoveEvent(event)

    def mousePressEventRoi(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.start_pos = self.mapToScene(event.pos())

            if self.roi:
                self.handle_index = self.roi.is_handle(self.start_pos)
                if self.handle_index:
                    self.handle_move_status = True
                    self.init_point = self.roi.center()
                    return
                if self.roi.is_in_roi(self.start_pos):
                    self.roi_move_status = True
                    self.init_point = self.roi.center()
                    return

            self.roi_select_status = True
            if self.roi is not None:
                self.roi.clear_from_scene(self.scene)

            scaleFactor = self.transform().m11()

            if self.roi_state == ROI.Rectangle:
                self.roi = RectangleRoi(scaleFactor)
                self.roi.setROI(self.start_pos.x(), self.start_pos.y(), 0, 0)
            elif self.roi_state == ROI.Line:
                self.roi = LineRoi(scaleFactor)
                self.roi.setROI(self.start_pos.x(), self.start_pos.y(), self.start_pos.x(), self.start_pos.y())
            elif self.roi_state == ROI.Circle:
                self.roi = CircleRoi(scaleFactor)
                self.roi.setROI(self.start_pos.x(), self.start_pos.y(), 0)
            elif self.roi_state == ROI.Ellipse:
                self.roi = EllipseRoi(scaleFactor)
                self.roi.setROI(self.start_pos.x(), self.start_pos.y(), 0, 0)
            self.scene.addItem(self.roi)
            self.roi.set_handles()

    def mouseMoveEventRoi(self, event: QMouseEvent):
        current_pos = self.mapToScene(event.pos())

        if self.roi:
            if self.roi.is_handle(current_pos):
                self.setCursor(Qt.CursorShape.PointingHandCursor)
            else:
                self.setCursor(Qt.CursorShape.ArrowCursor)

        if self.handle_move_status:
            self.setCursor(Qt.CursorShape.PointingHandCursor)
            self.roi.move_handle(current_pos, self.handle_index, self.start_pos, self.init_point)
            return

        if self.roi_move_status:
            self.roi.move_roi(current_pos, self.start_pos, self.init_point)
            return

        if self.roi_select_status:
            self.setCursor(Qt.CursorShape.CrossCursor)
            width = current_pos.x() - self.start_pos.x()
            height = current_pos.y() - self.start_pos.y()
            radius = int(math.sqrt(width ** 2 + height ** 2))
            if self.roi_state == ROI.Rectangle:
                self.roi.setROI(self.start_pos.x(), self.start_pos.y(), width, height)
            elif self.roi_state == ROI.Circle:
                self.roi.setROI(self.start_pos.x(), self.start_pos.y(), radius)
            elif self.roi_state == ROI.Line:
                if Qt.Key.Key_Shift in self.pressed_keys:
                    dx = abs(current_pos.x() - self.start_pos.x())
                    dy = abs(current_pos.y() - self.start_pos.y())
                    if dx >= dy:
                        current_pos.setY(self.start_pos.y())
                    else:
                        current_pos.setX(self.start_pos.x())
                self.roi.setROI(self.start_pos.x(), self.start_pos.y(), current_pos.x(), current_pos.y())
            elif self.roi_state == ROI.Ellipse:
                self.roi.setROI(self.start_pos.x(), self.start_pos.y(), width, height)

    def mouseReleaseEventRoi(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            end_pos = self.mapToScene(event.pos())
            if self.handle_move_status:
                self.handle_move_status = False
            elif self.roi_move_status:
                self.roi_move_status = False
                self.init_point = None
            else:
                if self.start_pos:
                    dis = math.sqrt((end_pos.x() - self.start_pos.x()) ** 2 + (end_pos.y() - self.start_pos.y()) ** 2)
                    scaleFactor = self.transform().m11()
                    if dis < (1 / scaleFactor) and self.roi:
                        self.roi.clear_from_scene(self.scene)
                        self.roi = None

            self.roi_select_status = False

            self.start_pos = None
            self.setCursor(Qt.CursorShape.ArrowCursor)

    def keyPressEvent(self, event: QKeyEvent):
        if self.image is None:
            return

        mouse_point = self.mapFromGlobal(QCursor.pos())
        mouse_point_scene = self.mapToScene(mouse_point)
        self.pressed_keys.append(event.key())

        width = self.viewport().width()
        height = self.viewport().height()

        hScale = mouse_point.x() / width
        vScale = mouse_point.y() / height

        scaleFactor = self.transform().m11()
        # 判断按下的是 "+" 键
        if event.key() == Qt.Key.Key_Equal or event.key() == Qt.Key.Key_Plus:
            # 图像放大操作

            factor = 1.2

            if scaleFactor >= self.initScale or factor == 1.2:
                self.scale(factor, factor)

            viewPoint = self.transform().map(mouse_point_scene)

            if self.roi is not None:
                scaleFactor = self.transform().m11()
                self.roi.scale_factor = scaleFactor

            self.horizontalScrollBar().setValue(int(viewPoint.x() - width * hScale))
            self.verticalScrollBar().setValue(int(viewPoint.y() - height * vScale))
        elif event.key() == Qt.Key.Key_Minus:
            # 图像缩小操作
            factor = 0.8

            if scaleFactor >= self.initScale or factor == 1.2:
                self.scale(factor, factor)

            viewPoint = self.transform().map(mouse_point_scene)

            if self.roi is not None:
                scaleFactor = self.transform().m11()
                self.roi.scale_factor = scaleFactor

            self.horizontalScrollBar().setValue(int(viewPoint.x() - width * hScale))
            self.verticalScrollBar().setValue(int(viewPoint.y() - height * vScale))
        elif event.key() == Qt.Key.Key_Left or event.key() == Qt.Key.Key_Right or event.key() == Qt.Key.Key_Up or event.key() == Qt.Key.Key_Down:
            if self.roi:
                self.roi.keyMove(event)
        else:
            # 其他键盘事件交给父类处理
            super().keyPressEvent(event)

    def keyReleaseEvent(self, event: QKeyEvent):
        self.pressed_keys.remove(event.key())
        super().keyReleaseEvent(event)

    def mousePressAngleEvent(self, event: QMouseEvent):
        pos = self.mapToScene(event.pos())
        if event.button() == Qt.MouseButton.LeftButton:
            if self.roi and len(self.points) == 0:
                self.start_pos = pos
                self.handle_index = self.roi.is_handle(pos)
                if self.handle_index:
                    self.handle_move_status = True
                    self.setCursor(Qt.CursorShape.PointingHandCursor)
                    return
                if self.roi.is_in_roi(pos):
                    self.roi_move_status = True
                    self.init_point = self.roi.get_corner_point()
                    self.setCursor(Qt.CursorShape.ArrowCursor)
                    return

            self.roi_select_status = True
            if self.roi is not None and len(self.points) == 0:
                self.roi.clear_from_scene(self.scene)

            scaleFactor = self.transform().m11()

            if len(self.points) == 0:
                self.roi = AngleRoi(scaleFactor)
                self.roi.add_to_scene(self.scene)

            self.points.append(pos)

            key = Qt.Key.Key_Shift if Qt.Key.Key_Shift in self.pressed_keys else None
            self.roi.setROI(pos.x(), pos.y(), len(self.points), key)

    def mouseMoveAngleEvent(self, event: QMouseEvent):
        current_pos = self.mapToScene(event.pos())

        if self.roi:
            if self.roi.is_handle(current_pos):
                self.setCursor(Qt.CursorShape.PointingHandCursor)
            else:
                self.setCursor(Qt.CursorShape.ArrowCursor)

        if self.handle_move_status:
            self.setCursor(Qt.CursorShape.PointingHandCursor)
            self.roi.move_handle(current_pos, self.handle_index, self.start_pos, self.init_point)
            return

        if self.roi_move_status:
            self.roi.move_roi(current_pos, self.start_pos, self.init_point)
            return

        if self.roi_select_status:
            self.setCursor(Qt.CursorShape.CrossCursor)
            key = Qt.Key.Key_Shift if Qt.Key.Key_Shift in self.pressed_keys else None
            self.roi.setROI(current_pos.x(), current_pos.y(), len(self.points) + 1, key)

    def mouseReleaseAngleEvent(self, event: QMouseEvent):
        end_pos = self.mapToScene(event.pos())

        if len(self.points) == 0 and event.button() == Qt.MouseButton.LeftButton:
            if self.handle_move_status:
                self.handle_move_status = False
            elif self.roi_move_status:
                self.roi_move_status = False

        if len(self.points) == 1 and self.start_pos and event.button() == Qt.MouseButton.LeftButton:
            dis = math.sqrt((end_pos.x() - self.start_pos.x()) ** 2 + (end_pos.y() - self.start_pos.y()) ** 2)
            scaleFactor = self.transform().m11()
            if dis < (1 / scaleFactor) and self.roi:
                self.roi.clear_from_scene(self.scene)
                self.roi = None

                self.roi_select_status = False
                self.start_pos = None
                self.points.clear()
                self.setCursor(Qt.CursorShape.ArrowCursor)

        if len(self.points) == 3 and event.button() == Qt.MouseButton.LeftButton:
            self.roi_select_status = False
            self.start_pos = None
            self.points.clear()
            self.setCursor(Qt.CursorShape.ArrowCursor)

    def mouseDoubleClickEvent(self, event):
        # print("double click")
        super().mouseDoubleClickEvent(event)
