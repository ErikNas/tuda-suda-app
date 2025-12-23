import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Item {
    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 20
        spacing: 15

        Label {
            text: "Стенды"
            font.pixelSize: 24
            font.bold: true
        }

        ListView {
            Layout.fillWidth: true
            Layout.fillHeight: true
            spacing: 8
            clip: true

            model: configController.stands

            delegate: Rectangle {
                width: ListView.view.width
                height: 60
                radius: 8
                color: "#3d3d3d"

                RowLayout {
                    anchors.fill: parent
                    anchors.margins: 12

                    ColumnLayout {
                        spacing: 2
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

                    Rectangle {
                        width: 12; height: 12; radius: 6
                        color: "#888888"  // Статус - заглушка
                    }
                }
            }
        }
    }
}
