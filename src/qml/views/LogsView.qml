import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Item {
    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 20

        Label {
            text: "Логи"
            font.pixelSize: 24
            font.bold: true
        }

        Label {
            text: "Здесь будут логи операций"
            color: "#888888"
        }

        Item { Layout.fillHeight: true }
    }
}

