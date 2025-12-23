import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Item {
    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 20
        spacing: 20

        Label {
            text: "Токен"
            font.pixelSize: 24
            font.bold: true
        }

        RowLayout {
            Layout.fillWidth: true
            spacing: 10

            ComboBox {
                id: standCombo
                Layout.preferredWidth: 200
                model: tokenController.stands
                enabled: !tokenController.loading
            }

            Button {
                text: tokenController.loading ? "Получение..." : "Получить токен"
                enabled: !tokenController.loading && standCombo.currentIndex >= 0
                onClicked: tokenController.fetch_token(standCombo.currentText)
            }
        }

        // Результат
        Rectangle {
            Layout.fillWidth: true
            Layout.preferredHeight: 120
            radius: 8
            color: "#3d3d3d"
            visible: tokenController.token || tokenController.error

            ColumnLayout {
                anchors.fill: parent
                anchors.margins: 15
                spacing: 10

                Label {
                    text: tokenController.error ? "Ошибка" : "Токен скопирован в буфер"
                    font.bold: true
                    color: tokenController.error ? "#F44336" : "#4CAF50"
                }

                TextArea {
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    text: tokenController.error || tokenController.token
                    readOnly: true
                    wrapMode: TextArea.Wrap
                    selectByMouse: true
                    background: Rectangle {
                        color: "#2d2d2d"
                        radius: 4
                    }
                }
            }
        }

        Item { Layout.fillHeight: true }
    }
}
