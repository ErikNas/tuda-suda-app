import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import "views"

ApplicationWindow {
    id: window
    visible: true
    width: 900
    height: 600
    minimumWidth: 700
    minimumHeight: 400
    title: "Tuda-Suda App"

    header: ToolBar {
        RowLayout {
            anchors.fill: parent
            anchors.leftMargin: 10
            anchors.rightMargin: 10

            Label {
                text: "Tuda-Suda App"
                font.bold: true
                font.pixelSize: 16
            }

            Item { Layout.fillWidth: true }

            // VPN индикаторы
            Row {
                spacing: 15

                Repeater {
                    model: vpnController.vpn_list

                    Row {
                        spacing: 5
                        Rectangle {
                            width: 12; height: 12; radius: 6
                            color: modelData.available === null ? "#888888" :
                                   modelData.available ? "#4CAF50" : "#F44336"
                        }
                        Label { text: modelData.name; font.pixelSize: 12 }
                    }
                }
            }
        }
    }

    RowLayout {
        anchors.fill: parent
        spacing: 0

        // Боковая навигация
        Rectangle {
            Layout.preferredWidth: 120
            Layout.fillHeight: true
            color: "#2d2d2d"

            ColumnLayout {
                anchors.fill: parent
                anchors.topMargin: 10
                spacing: 5

                Repeater {
                    model: ["Стенды", "Токен", "Роли", "Логи"]

                    Button {
                        Layout.fillWidth: true
                        Layout.leftMargin: 5
                        Layout.rightMargin: 5
                        text: modelData
                        flat: true
                        highlighted: stackView.currentIndex === index

                        onClicked: stackView.currentIndex = index
                    }
                }

                Item { Layout.fillHeight: true }
            }
        }

        // Основной контент
        StackLayout {
            id: stackView
            Layout.fillWidth: true
            Layout.fillHeight: true

            StandsView {}
            TokenView {}
            RolesView {}
            LogsView {}
        }
    }
}

