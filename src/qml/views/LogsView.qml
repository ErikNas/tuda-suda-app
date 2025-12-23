import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Item {
    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 20
        spacing: 15

        RowLayout {
            Layout.fillWidth: true

            Label {
                text: "Логи"
                font.pixelSize: 24
                font.bold: true
            }

            Item { Layout.fillWidth: true }

            Button {
                text: "Очистить"
                onClicked: logsController.clear()
            }
        }

        ScrollView {
            Layout.fillWidth: true
            Layout.fillHeight: true

            TextArea {
                id: logsArea
                text: logsController.logs_text
                readOnly: true
                selectByMouse: true
                font.family: "monospace"
                font.pixelSize: 12
                wrapMode: TextArea.Wrap
                background: Rectangle {
                    color: "#2d2d2d"
                    radius: 8
                }

                onTextChanged: {
                    cursorPosition = text.length
                }
            }
        }
    }
}
