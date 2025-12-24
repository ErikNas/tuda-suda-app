import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Effects
import "views"

ApplicationWindow {
    id: window
    visible: true
    width: 1000
    height: 700
    minimumWidth: 800
    minimumHeight: 500
    title: "Tuda-Suda"
    color: Theme.background

    // Шапка
    header: Rectangle {
        height: 48
        color: Theme.surface

        RowLayout {
            anchors.fill: parent
            anchors.leftMargin: 16
            anchors.rightMargin: 16
            spacing: 12

            // Лого / Название
            Label {
                text: "Tuda-Suda"
                font.pixelSize: 14
                font.weight: Font.DemiBold
                color: Theme.textPrimary
            }

            Item { Layout.fillWidth: true }

            // VPN индикаторы
            Row {
                spacing: 20

                Repeater {
                    model: vpnController.vpn_list

                    Row {
                        spacing: 8

                        Rectangle {
                            width: 10
                            height: 10
                            radius: 5
                            anchors.verticalCenter: parent.verticalCenter
                            color: modelData.available === null ? Theme.unknown :
                                   modelData.available ? Theme.successLight : Theme.errorLight

                            // Пульсация для активного VPN
                            SequentialAnimation on opacity {
                                running: modelData.available === null
                                loops: Animation.Infinite
                                NumberAnimation { to: 0.4; duration: 800 }
                                NumberAnimation { to: 1.0; duration: 800 }
                            }
                        }

                        Label {
                            text: modelData.name
                            font.pixelSize: 12
                            color: Theme.textSecondary
                            anchors.verticalCenter: parent.verticalCenter
                        }
                    }
                }
            }
        }

        // Нижняя граница
        Rectangle {
            anchors.bottom: parent.bottom
            width: parent.width
            height: 1
            color: Theme.border
        }
    }

    RowLayout {
        anchors.fill: parent
        spacing: 0

        // Боковая навигация
        Rectangle {
            Layout.preferredWidth: 180
            Layout.fillHeight: true
            color: Theme.navBackground

            ColumnLayout {
                anchors.fill: parent
                anchors.topMargin: 12
                anchors.bottomMargin: 12
                spacing: 4

                Repeater {
                    model: [
                        { name: "Стенды", icon: "🖥" },
                        { name: "Токен", icon: "🔑" },
                        { name: "Роли", icon: "👤" },
                        { name: "Логи", icon: "📋" }
                    ]

                    Rectangle {
                        Layout.fillWidth: true
                        Layout.preferredHeight: 40
                        Layout.leftMargin: 8
                        Layout.rightMargin: 8
                        radius: Theme.radiusMedium

                        property bool isActive: stackView.currentIndex === index
                        property bool isHovered: mouseArea.containsMouse

                        color: isActive ? Theme.navItemActive :
                               isHovered ? Theme.navItemHover : "transparent"

                        Behavior on color {
                            ColorAnimation { duration: Theme.animationFast }
                        }

                        RowLayout {
                            anchors.fill: parent
                            anchors.leftMargin: 12
                            anchors.rightMargin: 12
                            spacing: 10

                            Label {
                                text: modelData.icon
                                font.pixelSize: 16
                            }

                            Label {
                                text: modelData.name
                                font.pixelSize: 13
                                font.weight: parent.parent.isActive ? Font.DemiBold : Font.Normal
                                color: parent.parent.isActive ? Theme.textOnAccent : Theme.textPrimary
                                Layout.fillWidth: true
                            }

                            // Индикатор активности
                            Rectangle {
                                width: 3
                                height: 16
                                radius: 2
                                color: Theme.textOnAccent
                                visible: parent.parent.isActive
                            }
                        }

                        MouseArea {
                            id: mouseArea
                            anchors.fill: parent
                            hoverEnabled: true
                            cursorShape: Qt.PointingHandCursor
                            onClicked: stackView.currentIndex = index
                        }
                    }
                }

                Item { Layout.fillHeight: true }

                // Версия приложения внизу
                Label {
                    Layout.alignment: Qt.AlignHCenter
                    text: "v0.1.0"
                    font.pixelSize: 11
                    color: Theme.textDisabled
                }
            }

            // Правая граница
            Rectangle {
                anchors.right: parent.right
                anchors.top: parent.top
                anchors.bottom: parent.bottom
                width: 1
                color: Theme.border
            }
        }

        // Основной контент
        Rectangle {
            Layout.fillWidth: true
            Layout.fillHeight: true
            color: Theme.background

            StackLayout {
                id: stackView
                anchors.fill: parent

                StandsView {}
                TokenView {}
                RolesView {}
                LogsView {}
            }
        }
    }
}
