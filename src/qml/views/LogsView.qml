import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import ".."

Item {
    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 24
        spacing: 20

        // Заголовок
        RowLayout {
            Layout.fillWidth: true
            spacing: 16

            Label {
                text: "Логи"
                font.pixelSize: 28
                font.weight: Font.DemiBold
                color: Theme.textPrimary
            }

            Item { Layout.fillWidth: true }

            // Кнопка очистки
            Rectangle {
                width: clearBtnContent.width + 24
                height: 36
                radius: Theme.radiusMedium
                color: clearBtnArea.pressed ? Theme.cardPressed :
                       clearBtnArea.containsMouse ? Theme.cardHover : Theme.card
                border.width: 1
                border.color: Theme.border

                Behavior on color {
                    ColorAnimation { duration: Theme.animationFast }
                }

                Label {
                    id: clearBtnContent
                    anchors.centerIn: parent
                    text: "Очистить"
                    font.pixelSize: 13
                    color: Theme.textPrimary
                }

                MouseArea {
                    id: clearBtnArea
                    anchors.fill: parent
                    hoverEnabled: true
                    cursorShape: Qt.PointingHandCursor
                    onClicked: logsController.clear()
                }
            }
        }

        // Область логов
        Rectangle {
            Layout.fillWidth: true
            Layout.fillHeight: true
            radius: Theme.radiusLarge
            color: Theme.card

            ScrollView {
                anchors.fill: parent
                anchors.margins: 4

                TextArea {
                    id: logsArea
                    text: logsController.logs_text
                    readOnly: true
                    selectByMouse: true
                    font.family: "JetBrains Mono, Consolas, Monaco, monospace"
                    font.pixelSize: 12
                    wrapMode: TextArea.Wrap
                    color: Theme.textPrimary
                    padding: 12

                    background: Rectangle {
                        color: "transparent"
                    }

                    onTextChanged: {
                        cursorPosition = text.length
                    }
                }
            }

            // Пустое состояние
            Label {
                anchors.centerIn: parent
                text: "Логи пусты"
                font.pixelSize: 14
                color: Theme.textDisabled
                visible: logsController.logs_text === ""
            }
        }
    }
}
