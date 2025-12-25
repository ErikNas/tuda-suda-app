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
                text: "Стенды"
                font.pixelSize: 28
                font.weight: Font.DemiBold
                color: Theme.textPrimary
            }

            Item { Layout.fillWidth: true }

            // Кнопка обновления
            Rectangle {
                width: refreshRow.width + 24
                height: 36
                radius: Theme.radiusMedium
                color: mouseAreaRefresh.pressed ? Theme.accentPressed :
                       mouseAreaRefresh.containsMouse ? Theme.accentHover : Theme.accent

                Behavior on color {
                    ColorAnimation { duration: Theme.animationFast }
                }

                RowLayout {
                    id: refreshRow
                    anchors.centerIn: parent
                    spacing: 8

                    BusyIndicator {
                        Layout.preferredWidth: 16
                        Layout.preferredHeight: 16
                        running: standsController.loading
                        visible: standsController.loading
                    }

                    Label {
                        text: standsController.loading ? "Проверка..." : "Обновить"
                        font.pixelSize: 13
                        color: Theme.textOnAccent
                    }
                }

                MouseArea {
                    id: mouseAreaRefresh
                    anchors.fill: parent
                    hoverEnabled: true
                    cursorShape: Qt.PointingHandCursor
                    enabled: !standsController.loading
                    onClicked: standsController.refresh()
                }
            }
        }

        // Список стендов
        ListView {
            Layout.fillWidth: true
            Layout.fillHeight: true
            spacing: 12
            clip: true

            model: standsController.stands

            delegate: Rectangle {
                id: cardDelegate
                width: ListView.view.width
                height: 100
                radius: Theme.radiusLarge
                color: cardMouseArea.containsMouse ? Theme.cardHover : Theme.card

                Behavior on color {
                    ColorAnimation { duration: Theme.animationFast }
                }

                // Эффект при наведении - небольшое поднятие
                transform: Translate {
                    y: cardMouseArea.containsMouse ? -2 : 0
                    Behavior on y { NumberAnimation { duration: Theme.animationFast } }
                }

                MouseArea {
                    id: cardMouseArea
                    anchors.fill: parent
                    hoverEnabled: true
                }

                RowLayout {
                    anchors.fill: parent
                    anchors.margins: 16
                    spacing: 16

                    // Статус индикатор
                    Rectangle {
                        Layout.preferredWidth: 12
                        Layout.preferredHeight: 12
                        radius: 6
                        color: modelData.status === "online" ? Theme.successLight :
                               modelData.status === "offline" ? Theme.errorLight : Theme.unknown

                        // Пульсация для unknown
                        SequentialAnimation on opacity {
                            running: modelData.status === "unknown"
                            loops: Animation.Infinite
                            NumberAnimation { to: 0.4; duration: 800 }
                            NumberAnimation { to: 1.0; duration: 800 }
                        }
                    }

                    // Информация о стенде
                    ColumnLayout {
                        Layout.fillWidth: true
                        spacing: 6

                        Label {
                            text: modelData.name
                            font.pixelSize: 16
                            font.weight: Font.DemiBold
                            color: Theme.textPrimary
                        }

                        Label {
                            text: modelData.api_url
                            font.pixelSize: 12
                            color: Theme.textSecondary
                            elide: Text.ElideMiddle
                            Layout.fillWidth: true
                        }

                        // Тег и ветка
                        RowLayout {
                            spacing: 12
                            visible: modelData.status === "online"

                            Label {
                                text: "🏷️ " + modelData.tag
                                font.pixelSize: 11
                                color: Theme.textSecondary
                            }

                            Label {
                                text: "🌿 " + modelData.branch
                                font.pixelSize: 11
                                color: Theme.textSecondary
                            }
                        }

                        // Ссылки на Swagger
                        RowLayout {
                            spacing: 16

                            // Core Swagger
                            Label {
                                text: "Core Swagger ↗"
                                font.pixelSize: 12
                                color: swaggerCoreArea.containsMouse ? Theme.accentLight : Theme.accent
                                visible: modelData.core_swagger_url !== ""

                                Behavior on color {
                                    ColorAnimation { duration: Theme.animationFast }
                                }

                                MouseArea {
                                    id: swaggerCoreArea
                                    anchors.fill: parent
                                    hoverEnabled: true
                                    cursorShape: Qt.PointingHandCursor
                                    onClicked: Qt.openUrlExternally(modelData.core_swagger_url)
                                }
                            }

                            // External Swagger
                            Label {
                                text: "External Swagger ↗"
                                font.pixelSize: 12
                                color: swaggerExtArea.containsMouse ? Theme.accentLight : Theme.accent
                                visible: modelData.external_swagger_url !== ""

                                Behavior on color {
                                    ColorAnimation { duration: Theme.animationFast }
                                }

                                MouseArea {
                                    id: swaggerExtArea
                                    anchors.fill: parent
                                    hoverEnabled: true
                                    cursorShape: Qt.PointingHandCursor
                                    onClicked: Qt.openUrlExternally(modelData.external_swagger_url)
                                }
                            }
                        }
                    }

                    // Версия
                    Rectangle {
                        Layout.preferredWidth: versionLabel.width + 16
                        Layout.preferredHeight: 28
                        radius: Theme.radiusSmall
                        color: Theme.surface
                        visible: modelData.version !== "—"

                        Label {
                            id: versionLabel
                            anchors.centerIn: parent
                            text: modelData.version
                            font.pixelSize: 12
                            font.family: "monospace"
                            color: Theme.textSecondary
                        }
                    }
                }
            }
        }
    }
}
