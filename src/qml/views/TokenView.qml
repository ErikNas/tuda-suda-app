import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Item {
    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 20

        Label {
            text: "Токен"
            font.pixelSize: 24
            font.bold: true
        }

        Label {
            text: "Здесь будет получение токена"
            color: "#888888"
        }

        Item { Layout.fillHeight: true }
    }
}

