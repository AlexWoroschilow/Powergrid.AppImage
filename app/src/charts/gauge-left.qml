import QtQuick 2.0
import QtQuick.Controls 1.4
import QtQuick.Controls.Styles 1.4
import QtQuick.Extras 1.4
import QtQuick.Extras.Private 1.0

CircularGauge {
    property real load: 0.0
    objectName: "performance"
    minimumValue: 0
    value: load
    maximumValue: 100

    style: CircularGaugeStyle {
		minimumValueAngle: -130
		maximumValueAngle: 90
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
            color: styleData.value >= 80 ? "#e34c22" : styleData.value <= 40 ? "#62C106" : "#ffa500"
        }

        minorTickmark: Rectangle {
            visible: styleData.value < 80
            implicitWidth: outerRadius * 0.01
            antialiasing: true
            implicitHeight: outerRadius * 0.03
            color: "#8a8a8a"
        }

        tickmarkLabel:  Text {
            font.pixelSize: Math.max(12, outerRadius * 0.1)
            text: styleData.value
            color: styleData.value >= 80 ? "#e34c22" : styleData.value <= 40 ? "#62C106" : "#ffa500"
            antialiasing: true
        }

        function degreesToRadians(degrees) {
            return degrees * (Math.PI / 180);
        }

        background: Canvas {
            onPaint: {
                var ctx = getContext("2d");
                ctx.reset();

                ctx.beginPath();
                ctx.strokeStyle = "#e34c22";
                ctx.lineWidth = outerRadius * 0.02;

                ctx.arc(outerRadius, outerRadius, outerRadius - ctx.lineWidth / 2,
                    degreesToRadians(valueToAngle(80) - 90), degreesToRadians(valueToAngle(100) - 90));
                ctx.stroke();
            }
        }

    }

    Text {
        id: frequency
        property string title: "... GHz"
        font.pixelSize: 44
        objectName: "title"
        text: title
        anchors.right: parent.right
        anchors.bottom: parent.bottom
        color: "#5E5E5E"
    }

    Text {
        font.pixelSize: 14
        text: "CPU frequency"
        anchors.right: parent.right
        anchors.bottom: frequency.top
        color: "#8a8a8a"
    }



      Behavior on value {
          NumberAnimation {
              duration: 1000
          }
      }    
}