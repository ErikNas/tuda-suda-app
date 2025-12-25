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
            text: "Токен"
            font.pixelSize: 28
            font.weight: Font.DemiBold
            color: Theme.textPrimary
        }

        // Форма
        Rectangle {
            Layout.fillWidth: true
            Layout.preferredHeight: formLayout.height + 32
            radius: Theme.radiusLarge
            color: Theme.card

            ColumnLayout {
                id: formLayout
                anchors.left: parent.left
                anchors.right: parent.right
                anchors.top: parent.top
                anchors.margins: 16
                spacing: 16

                Label {
                    text: "Выберите стенд для получения токена"
                    font.pixelSize: 13
                    color: Theme.textSecondary
                }

                // Стенд
                Rectangle {
                    Layout.fillWidth: true
                    Layout.preferredHeight: 40
                    radius: Theme.radiusMedium
                    color: comboMouseArea.containsMouse ? Theme.inputBackgroundHover : Theme.inputBackground
                    border.width: standCombo.activeFocus ? 2 : 1
                    border.color: standCombo.activeFocus ? Theme.borderFocus : Theme.border

                    Behavior on color {
                        ColorAnimation { duration: Theme.animationFast }
                    }

                    ComboBox {
                        id: standCombo
                        anchors.fill: parent
                        anchors.margins: 1
                        model: tokenController.stands
                        enabled: !tokenController.loading
                        font.pixelSize: 13

                        background: Rectangle {
                            color: "transparent"
                        }

                        contentItem: Label {
                            leftPadding: 12
                            text: standCombo.displayText
                            font: standCombo.font
                            color: Theme.textPrimary
                            verticalAlignment: Text.AlignVCenter
                        }
                    }

                    MouseArea {
                        id: comboMouseArea
                        anchors.fill: parent
                        hoverEnabled: true
                        acceptedButtons: Qt.NoButton
                    }
                }

                // Логин
                Label {
                    text: "Логин"
                    font.pixelSize: 13
                    color: Theme.textSecondary
                }

                Rectangle {
                    Layout.fillWidth: true
                    Layout.preferredHeight: 40
                    radius: Theme.radiusMedium
                    color: loginMouseArea.containsMouse ? Theme.inputBackgroundHover : Theme.inputBackground
                    border.width: loginField.activeFocus ? 2 : 1
                    border.color: loginField.activeFocus ? Theme.borderFocus : Theme.border

                    Behavior on color {
                        ColorAnimation { duration: Theme.animationFast }
                    }

                    TextInput {
                        id: loginField
                        anchors.fill: parent
                        anchors.leftMargin: 12
                        anchors.rightMargin: 12
                        font.pixelSize: 13
                        color: Theme.textPrimary
                        verticalAlignment: TextInput.AlignVCenter
                        enabled: !tokenController.loading
                        selectByMouse: true
                    }

                    MouseArea {
                        id: loginMouseArea
                        anchors.fill: parent
                        hoverEnabled: true
                        acceptedButtons: Qt.NoButton
                    }
                }

                // Пароль
                Label {
                    text: "Пароль"
                    font.pixelSize: 13
                    color: Theme.textSecondary
                }

                Rectangle {
                    Layout.fillWidth: true
                    Layout.preferredHeight: 40
                    radius: Theme.radiusMedium
                    color: passwordMouseArea.containsMouse ? Theme.inputBackgroundHover : Theme.inputBackground
                    border.width: passwordField.activeFocus ? 2 : 1
                    border.color: passwordField.activeFocus ? Theme.borderFocus : Theme.border

                    Behavior on color {
                        ColorAnimation { duration: Theme.animationFast }
                    }

                    TextInput {
                        id: passwordField
                        anchors.fill: parent
                        anchors.leftMargin: 12
                        anchors.rightMargin: 12
                        font.pixelSize: 13
                        color: Theme.textPrimary
                        echoMode: TextInput.Password
                        verticalAlignment: TextInput.AlignVCenter
                        enabled: !tokenController.loading
                        selectByMouse: true
                    }

                    MouseArea {
                        id: passwordMouseArea
                        anchors.fill: parent
                        hoverEnabled: true
                        acceptedButtons: Qt.NoButton
                    }
                }

                RowLayout {
                    Layout.fillWidth: true
                    spacing: 12

                    Item { Layout.fillWidth: true }

                    // Кнопка получения токена
                    Rectangle {
                        Layout.preferredWidth: btnContent.width + 32
                        Layout.preferredHeight: 40
                        radius: Theme.radiusMedium
                        color: !btnMouseArea.enabled ? Theme.textDisabled :
                               btnMouseArea.pressed ? Theme.accentPressed :
                               btnMouseArea.containsMouse ? Theme.accentHover : Theme.accent

                        Behavior on color {
                            ColorAnimation { duration: Theme.animationFast }
                        }

                        RowLayout {
                            id: btnContent
                            anchors.centerIn: parent
                            spacing: 8

                            BusyIndicator {
                                Layout.preferredWidth: 16
                                Layout.preferredHeight: 16
                                running: tokenController.loading
                                visible: tokenController.loading
                            }

                            Label {
                                text: tokenController.loading ? "Получение..." : "Получить токен"
                                font.pixelSize: 13
                                font.weight: Font.Medium
                                color: Theme.textOnAccent
                            }
                        }

                        MouseArea {
                            id: btnMouseArea
                            anchors.fill: parent
                            hoverEnabled: true
                            cursorShape: enabled ? Qt.PointingHandCursor : Qt.ArrowCursor
                            enabled: !tokenController.loading && standCombo.currentIndex >= 0
                            onClicked: tokenController.fetch_token(
                                standCombo.currentText,
                                loginField.text,
                                passwordField.text
                            )
                        }
                    }
                }
            }
        }

        // Результат
        Rectangle {
            Layout.fillWidth: true
            Layout.preferredHeight: 150
            radius: Theme.radiusLarge
            color: Theme.card
            visible: tokenController.token || tokenController.error

            ColumnLayout {
                anchors.fill: parent
                anchors.margins: 16
                spacing: 12

                RowLayout {
                    spacing: 8

                    Rectangle {
                        width: 8
                        height: 8
                        radius: 4
                        color: tokenController.error ? Theme.errorLight : Theme.successLight
                    }

                    Label {
                        text: tokenController.error ? "Ошибка" : "Токен скопирован в буфер"
                        font.pixelSize: 14
                        font.weight: Font.DemiBold
                        color: tokenController.error ? Theme.errorLight : Theme.successLight
                    }
                }

                Rectangle {
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    radius: Theme.radiusMedium
                    color: Theme.surface

                    ScrollView {
                        anchors.fill: parent
                        anchors.margins: 8

                        TextArea {
                            text: tokenController.error || tokenController.token
                            readOnly: true
                            wrapMode: TextArea.Wrap
                            selectByMouse: true
                            font.pixelSize: 12
                            font.family: "monospace"
                            color: Theme.textPrimary

                            background: Rectangle {
                                color: "transparent"
                            }
                        }
                    }
                }
            }
        }

        Item { Layout.fillHeight: true }
    }
}
