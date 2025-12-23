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
                text: "Стенды"
                font.pixelSize: 24
                font.bold: true
            }

            Item { Layout.fillWidth: true }

            Button {
                text: standsController.loading ? "Проверка..." : "Обновить"
                enabled: !standsController.loading
                onClicked: standsController.refresh()
            }
        }

        ListView {
            Layout.fillWidth: true
            Layout.fillHeight: true
            spacing: 8
            clip: true

            model: standsController.stands

            delegate: Rectangle {
                width: ListView.view.width
                height: 60
                radius: 8
                color: "#3d3d3d"

                RowLayout {
                    anchors.fill: parent
                    anchors.margins: 12

                    Rectangle {
                        width: 12; height: 12; radius: 6
                        color: modelData.status === "online" ? "#4CAF50" :
                               modelData.status === "offline" ? "#F44336" : "#888888"
                    }

                    ColumnLayout {
                        spacing: 2
                        Layout.leftMargin: 8

                        Label {
                            text: modelData.name
                            font.bold: true
                            font.pixelSize: 14
                        }
                        Label {
                            text: modelData.api_url
                            font.pixelSize: 11
                            color: "#888888"
                        }
                    }

                    Item { Layout.fillWidth: true }

                    Label {
                        text: modelData.version
                        font.pixelSize: 12
                        color: "#aaaaaa"
                    }
                }
            }
        }
    }
}
