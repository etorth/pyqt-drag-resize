import sys

from PyQt6.QtCore import Qt, QRectF, QPointF, QLineF
from PyQt6.QtGui import QBrush, QPainterPath, QPainter, QColor, QPen, QPixmap
from PyQt6.QtWidgets import QGraphicsRectItem, QApplication, QGraphicsView, QGraphicsScene, QGraphicsItem


class GraphicsRectItem(QGraphicsRectItem):
    dragDistance = 8.0

    handleTopLeft = 1
    handleTopMiddle = 2
    handleTopRight = 3
    handleMiddleLeft = 4
    handleMiddleRight = 5
    handleBottomLeft = 6
    handleBottomMiddle = 7
    handleBottomRight = 8

    handleCursors = {
        handleTopLeft: Qt.CursorShape.SizeFDiagCursor,
        handleTopMiddle: Qt.CursorShape.SizeVerCursor,
        handleTopRight: Qt.CursorShape.SizeBDiagCursor,
        handleMiddleLeft: Qt.CursorShape.SizeHorCursor,
        handleMiddleRight: Qt.CursorShape.SizeHorCursor,
        handleBottomLeft: Qt.CursorShape.SizeBDiagCursor,
        handleBottomMiddle: Qt.CursorShape.SizeVerCursor,
        handleBottomRight: Qt.CursorShape.SizeFDiagCursor,
    }


    def __init__(self, *args):
        super().__init__(*args)
        self.handleSelected = None
        self.mousePressPos = None
        self.mousePressRect = None
        self.setAcceptHoverEvents(True)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges, True)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsFocusable, True)


    def handleAt(self, point):
        b = self.boundingRect()
        if b.contains(point):
            if QLineF(point, b.topLeft    ()).length() <= self.dragDistance: return self.handleTopLeft
            if QLineF(point, b.topRight   ()).length() <= self.dragDistance: return self.handleTopRight
            if QLineF(point, b.bottomLeft ()).length() <= self.dragDistance: return self.handleBottomLeft
            if QLineF(point, b.bottomRight()).length() <= self.dragDistance: return self.handleBottomRight

            if abs(point.x() - b.left  ()) <= self.dragDistance: return self.handleMiddleLeft
            if abs(point.x() - b.right ()) <= self.dragDistance: return self.handleMiddleRight
            if abs(point.y() - b.top   ()) <= self.dragDistance: return self.handleTopMiddle
            if abs(point.y() - b.bottom()) <= self.dragDistance: return self.handleBottomMiddle
        return None


    def hoverMoveEvent(self, moveEvent):
        if self.isSelected():
            handle = self.handleAt(moveEvent.pos())
            if handle is None:
                cursor = Qt.CursorShape.ArrowCursor
            else:
                cursor = self.handleCursors[handle]
            self.setCursor(cursor)
        super().hoverMoveEvent(moveEvent)


    def hoverLeaveEvent(self, moveEvent):
        self.setCursor(Qt.CursorShape.ArrowCursor)
        super().hoverLeaveEvent(moveEvent)


    def mousePressEvent(self, mouseEvent):
        self.handleSelected = self.handleAt(mouseEvent.pos())
        if self.handleSelected:
            self.mousePressPos = mouseEvent.pos()
            self.mousePressRect = self.boundingRect()
        super().mousePressEvent(mouseEvent)


    def mouseMoveEvent(self, mouseEvent):
        if self.handleSelected is None:
            super().mouseMoveEvent(mouseEvent)
        else:
            self.interactiveResize(mouseEvent.pos())


    def mouseReleaseEvent(self, mouseEvent):
        super().mouseReleaseEvent(mouseEvent)
        self.handleSelected = None
        self.mousePressPos = None
        self.mousePressRect = None
        self.update()


    def interactiveResize(self, mousePos):
        self.prepareGeometryChange()
        rect = self.rect()

        if self.handleSelected == self.handleTopLeft:
            rect.setLeft(self.mousePressRect.left() + mousePos.x() - self.mousePressPos.x())
            rect.setTop(self.mousePressRect.top() + mousePos.y() - self.mousePressPos.y())
            self.setRect(rect)

        elif self.handleSelected == self.handleTopMiddle:
            rect.setTop(self.mousePressRect.top() + mousePos.y() - self.mousePressPos.y())
            self.setRect(rect)

        elif self.handleSelected == self.handleTopRight:
            rect.setRight(self.mousePressRect.right() + mousePos.x() - self.mousePressPos.x())
            rect.setTop(self.mousePressRect.top() + mousePos.y() - self.mousePressPos.y())
            self.setRect(rect)

        elif self.handleSelected == self.handleMiddleLeft:
            rect.setLeft(self.mousePressRect.left() + mousePos.x() - self.mousePressPos.x())
            self.setRect(rect)

        elif self.handleSelected == self.handleMiddleRight:
            rect.setRight(self.mousePressRect.right() + mousePos.x() - self.mousePressPos.x())
            self.setRect(rect)

        elif self.handleSelected == self.handleBottomLeft:
            rect.setLeft(self.mousePressRect.left() + mousePos.x() - self.mousePressPos.x())
            rect.setBottom(self.mousePressRect.bottom() + mousePos.y() - self.mousePressPos.y())
            self.setRect(rect)

        elif self.handleSelected == self.handleBottomMiddle:
            rect.setBottom(self.mousePressRect.bottom() + mousePos.y() - self.mousePressPos.y())
            self.setRect(rect)

        elif self.handleSelected == self.handleBottomRight:
            rect.setRight(self.mousePressRect.right() + mousePos.x() - self.mousePressPos.x())
            rect.setBottom(self.mousePressRect.bottom() + mousePos.y() - self.mousePressPos.y())
            self.setRect(rect)


    def paint(self, painter, option, widget=None):
        if self.isSelected():
            painter.setBrush(QBrush(QColor(0, 0, 255, 100)))
        else:
            painter.setBrush(QBrush(QColor(255, 0, 0, 100)))

        painter.setPen(QPen(QColor(0, 0, 0), 1.0, Qt.PenStyle.SolidLine))
        painter.drawRect(self.rect())


def main():

    app = QApplication(sys.argv)

    scene = QGraphicsScene()
    scene.setSceneRect(0, 0, 800, 600)

    grview = QGraphicsView()
    grview.setScene(scene)

    item = GraphicsRectItem(0, 0, 300, 150)
    scene.addItem(item)

    grview.fitInView(scene.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)
    grview.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
