import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import ".."

Item {
    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 24
        spacing: 24

        // Заголовок
        Label {
            text: "Управление ролями"
            font.pixelSize: 28
            font.weight: Font.DemiBold
            color: Theme.textPrimary
        }

        // Форма
        Rectangle {
            Layout.fillWidth: true
            Layout.preferredHeight: formContent.height + 32
            radius: Theme.radiusLarge
            color: Theme.card

            ColumnLayout {
                id: formContent
                anchors.left: parent.left
                anchors.right: parent.right
                anchors.top: parent.top
                anchors.margins: 16
                spacing: 20

                // Выбор стенда
                ColumnLayout {
                    spacing: 8

                    Label {
                        text: "Стенд"
                        font.pixelSize: 13
                        color: Theme.textSecondary
                    }

                    Rectangle {
                        Layout.preferredWidth: 300
                        Layout.preferredHeight: 40
                        radius: Theme.radiusMedium
                        color: standComboArea.containsMouse ? Theme.inputBackgroundHover : Theme.inputBackground
                        border.width: standCombo.activeFocus ? 2 : 1
                        border.color: standCombo.activeFocus ? Theme.borderFocus : Theme.border

                        ComboBox {
                            id: standCombo
                            anchors.fill: parent
                            anchors.margins: 1
                            model: rolesController.stands
                            enabled: !rolesController.loading
                            font.pixelSize: 13

                            background: Rectangle { color: "transparent" }

                            contentItem: Label {
                                leftPadding: 12
                                text: standCombo.displayText
                                font: standCombo.font
                                color: Theme.textPrimary
                                verticalAlignment: Text.AlignVCenter
                            }
                        }

                        MouseArea {
                            id: standComboArea
                            anchors.fill: parent
                            hoverEnabled: true
                            acceptedButtons: Qt.NoButton
                        }
                    }
                }

                // Email
                ColumnLayout {
                    spacing: 8

                    Label {
                        text: "Email пользователя"
                        font.pixelSize: 13
                        color: Theme.textSecondary
                    }

                    Rectangle {
                        Layout.preferredWidth: 400
                        Layout.preferredHeight: 40
                        radius: Theme.radiusMedium
                        color: emailFieldArea.containsMouse ? Theme.inputBackgroundHover : Theme.inputBackground
                        border.width: emailField.activeFocus ? 2 : 1
                        border.color: emailField.activeFocus ? Theme.borderFocus : Theme.border

                        Behavior on border.color {
                            ColorAnimation { duration: Theme.animationFast }
                        }

                        TextField {
                            id: emailField
                            anchors.fill: parent
                            anchors.margins: 1
                            placeholderText: "user@example.com"
                            placeholderTextColor: Theme.textDisabled
                            enabled: !rolesController.loading
                            font.pixelSize: 13
                            color: Theme.textPrimary
                            leftPadding: 12

                            background: Rectangle { color: "transparent" }
                        }

                        MouseArea {
                            id: emailFieldArea
                            anchors.fill: parent
                            hoverEnabled: true
                            acceptedButtons: Qt.NoButton
                        }
                    }
                }

                // Кнопки действий
                RowLayout {
                    spacing: 12

                    // Сделать админом
                    Rectangle {
                        Layout.preferredWidth: adminBtnContent.width + 32
                        Layout.preferredHeight: 40
                        radius: Theme.radiusMedium
                        color: !adminBtnArea.enabled ? Theme.textDisabled :
                               adminBtnArea.pressed ? Theme.accentPressed :
                               adminBtnArea.containsMouse ? Theme.accentHover : Theme.accent

                        Behavior on color {
                            ColorAnimation { duration: Theme.animationFast }
                        }

                        Label {
                            id: adminBtnContent
                            anchors.centerIn: parent
                            text: "Сделать админом"
                            font.pixelSize: 13
                            font.weight: Font.Medium
                            color: Theme.textOnAccent
                        }

                        MouseArea {
                            id: adminBtnArea
                            anchors.fill: parent
                            hoverEnabled: true
                            cursorShape: enabled ? Qt.PointingHandCursor : Qt.ArrowCursor
                            enabled: !rolesController.loading && emailField.text.length > 0
                            onClicked: rolesController.change_role(standCombo.currentText, emailField.text, "admin")
                        }
                    }

                    // Сделать юзером
                    Rectangle {
                        Layout.preferredWidth: userBtnContent.width + 32
                        Layout.preferredHeight: 40
                        radius: Theme.radiusMedium
                        color: !userBtnArea.enabled ? Theme.textDisabled :
                               userBtnArea.pressed ? Theme.cardPressed :
                               userBtnArea.containsMouse ? Theme.cardHover : Theme.card
                        border.width: 1
                        border.color: Theme.border

                        Behavior on color {
                            ColorAnimation { duration: Theme.animationFast }
                        }

                        Label {
                            id: userBtnContent
                            anchors.centerIn: parent
                            text: "Сделать юзером"
                            font.pixelSize: 13
                            font.weight: Font.Medium
                            color: Theme.textPrimary
                        }

                        MouseArea {
                            id: userBtnArea
                            anchors.fill: parent
                            hoverEnabled: true
                            cursorShape: enabled ? Qt.PointingHandCursor : Qt.ArrowCursor
                            enabled: !rolesController.loading && emailField.text.length > 0
                            onClicked: rolesController.change_role(standCombo.currentText, emailField.text, "user")
                        }
                    }

                    BusyIndicator {
                        Layout.preferredWidth: 24
                        Layout.preferredHeight: 24
                        running: rolesController.loading
                        visible: rolesController.loading
                    }
                }
            }
        }

        // Результат
        Rectangle {
            Layout.fillWidth: true
            Layout.preferredHeight: 56
            radius: Theme.radiusLarge
            color: Theme.card
            visible: rolesController.result

            RowLayout {
                anchors.fill: parent
                anchors.margins: 16
                spacing: 12

                Rectangle {
                    width: 8
                    height: 8
                    radius: 4
                    color: rolesController.is_error ? Theme.errorLight : Theme.successLight
                }

                Label {
                    text: rolesController.result
                    font.pixelSize: 14
                    color: rolesController.is_error ? Theme.errorLight : Theme.successLight
                    Layout.fillWidth: true
                }
            }
        }

        Item { Layout.fillHeight: true }
    }
}
