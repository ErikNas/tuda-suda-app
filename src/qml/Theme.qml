pragma Singleton
import QtQuick 2.15

QtObject {
    // Акцентные цвета
    readonly property color accent: "#0078D4"
    readonly property color accentLight: "#1890FF"
    readonly property color accentHover: "#106EBE"
    readonly property color accentPressed: "#005A9E"

    // Фоны
    readonly property color background: "#1A1A1A"
    readonly property color surface: "#202020"
    readonly property color card: "#2D2D2D"
    readonly property color cardHover: "#383838"
    readonly property color cardPressed: "#404040"

    // Навигация
    readonly property color navBackground: "#1C1C1C"
    readonly property color navItemHover: "#333333"
    readonly property color navItemActive: "#0078D4"

    // Текст
    readonly property color textPrimary: "#FFFFFF"
    readonly property color textSecondary: "#A0A0A0"
    readonly property color textDisabled: "#606060"
    readonly property color textOnAccent: "#FFFFFF"

    // Статусы
    readonly property color success: "#0F7B0F"
    readonly property color successLight: "#4CAF50"
    readonly property color error: "#D13438"
    readonly property color errorLight: "#F44336"
    readonly property color warning: "#FCE100"
    readonly property color unknown: "#6E6E6E"

    // Границы
    readonly property color border: "#404040"
    readonly property color borderHover: "#606060"
    readonly property color borderFocus: "#0078D4"

    // Поля ввода
    readonly property color inputBackground: "#2D2D2D"
    readonly property color inputBackgroundHover: "#383838"

    // Размеры
    readonly property int radiusSmall: 4
    readonly property int radiusMedium: 8
    readonly property int radiusLarge: 12

    // Анимации
    readonly property int animationFast: 100
    readonly property int animationNormal: 200
    readonly property int animationSlow: 300
}
