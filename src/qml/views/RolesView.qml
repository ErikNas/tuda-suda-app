import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Item {
    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 20
        spacing: 20

        Label {
            text: "Роли"
            font.pixelSize: 24
            font.bold: true
        }

        GridLayout {
            columns: 2
            columnSpacing: 10
            rowSpacing: 15

            Label { text: "Стенд:" }
            ComboBox {
                id: standCombo
                Layout.preferredWidth: 200
                model: rolesController.stands
                enabled: !rolesController.loading
            }

            Label { text: "Email:" }
            TextField {
                id: emailField
                Layout.preferredWidth: 300
                placeholderText: "user@example.com"
                enabled: !rolesController.loading
            }
        }

        RowLayout {
            spacing: 10

            Button {
                text: "Сделать админом"
                enabled: !rolesController.loading && emailField.text
                onClicked: rolesController.change_role(standCombo.currentText, emailField.text, "admin")
            }

            Button {
                text: "Сделать юзером"
                enabled: !rolesController.loading && emailField.text
                onClicked: rolesController.change_role(standCombo.currentText, emailField.text, "user")
            }

            BusyIndicator {
                running: rolesController.loading
                visible: rolesController.loading
            }
        }

        // Результат
        Rectangle {
            Layout.fillWidth: true
            Layout.preferredHeight: 50
            radius: 8
            color: "#3d3d3d"
            visible: rolesController.result

            Label {
                anchors.centerIn: parent
                text: rolesController.result
                color: rolesController.is_error ? "#F44336" : "#4CAF50"
                font.pixelSize: 14
            }
        }

        Item { Layout.fillHeight: true }
    }
}
