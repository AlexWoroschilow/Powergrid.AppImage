import QtQuick 2.0
import QtQuick.Controls 1.4
import QtQuick.Controls.Styles 1.4
import QtQuick.Extras 1.4
import QtQuick.Extras.Private 1.0

CircularGauge {
    property real load: 0.0
    objectName: "performance"
    minimumValue: 0
    maximumValue: 100
    value: load

    style: CircularGaugeStyle {
		minimumValueAngle: 180
		maximumValueAngle: 20
        needle: Rectangle {
            y: outerRadius * 0.15
            implicitWidth: outerRadius * 0.03
            implicitHeight: outerRadius * 0.85
            antialiasing: true
            color: "#8a8a8a"
        }

        tickmark: Rectangle {
            implicitWidth: outerRadius * 0.02
            antialiasing: true
            implicitHeight: outerRadius * 0.07
            color: styleData.value >= 80 ? "#62C106" : styleData.value <= 25 ? "#e34c22" : "#ffa500"
        }

        minorTickmark: Rectangle {
            implicitWidth: outerRadius * 0.01
            antialiasing: true
            implicitHeight: outerRadius * 0.03
            color: "#8a8a8a"
        }

        tickmarkLabel:  Text {
            visible: (styleData.value % 20) == 0
            font.pixelSize: Math.max(10, outerRadius * 0.1)
            text: styleData.value
            color: styleData.value >= 80 ? "#62C106" : styleData.value <= 25 ? "#e34c22" : "#ffa500"
            antialiasing: true
        }

        function degreesToRadians(degrees) {
            return degrees * (Math.PI / 180);
        }
    }

    Text {
        text: "Bat."
        font.pixelSize: 9
        anchors.left: parent.horizontalCenter
        anchors.top: parent.verticalCenter
        color: "#8a8a8a"
    }

      Behavior on value {
          NumberAnimation {
              duration: 1000
          }
      }    
}