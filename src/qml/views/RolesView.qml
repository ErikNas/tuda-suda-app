import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Item {
    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 20

        Label {
            text: "Роли"
            font.pixelSize: 24
            font.bold: true
        }

        Label {
            text: "Здесь будет управление ролями"
            color: "#888888"
        }

        Item { Layout.fillHeight: true }
    }
}

