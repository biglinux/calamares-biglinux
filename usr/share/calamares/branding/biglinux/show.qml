import QtQuick 2.0;
import calamares.slideshow 1.0;

Presentation
{
    id: presentation

    Timer {
        interval: 17000
        running: true
        repeat: true
        onTriggered: presentation.goToNextSlide()
    }
Slide 
{
        anchors.fill: parent

        Image {
            id: background
            source: "pt/00.jpg"
            anchors.fill: parent
        
        }
}   
Slide 
{
        anchors.fill: parent

        Image {
            id: background1
            source: "pt/01.jpg"
            anchors.fill: parent
        
        }
}   
Slide 
{
        anchors.fill: parent

        Image {
            id: background2
            source: "pt/02.jpg"
            anchors.fill: parent
        
    }
}   
Slide 
{
        anchors.fill: parent

        Image {
            id: background3
            source: "pt/03.jpg"
            anchors.fill: parent
        
        }
    }

Slide 
{
        anchors.fill: parent

        Image {
            id: background4
            source: "pt/04.jpg"
            anchors.fill: parent
        
    }
}   


Slide 
{
        anchors.fill: parent

        Image {
            id: background5
            source: "pt/05.jpg"
            anchors.fill: parent
        
    }
}   


Slide 
{
        anchors.fill: parent

        Image {
            id: background6
            source: "pt/06.jpg"
            anchors.fill: parent
        
    }
}   


Slide 
{
        anchors.fill: parent

        Image {
            id: background7
            source: "pt/07.jpg"
            anchors.fill: parent
        
    }
}   


Slide 
{
        anchors.fill: parent

        Image {
            id: background8
            source: "pt/08.jpg"
            anchors.fill: parent
        
    }
}


Slide 
{
        anchors.fill: parent

        Image {
            id: background9
            source: "pt/09.jpg"
            anchors.fill: parent
        
    }
} 


Slide 
{
        anchors.fill: parent

        Image {
            id: background10
            source: "pt/10.jpg"
            anchors.fill: parent
        
    }
} 


Slide 
{
        anchors.fill: parent

        Image {
            id: background11
            source: "pt/11.jpg"
            anchors.fill: parent
        
    }
} 


Slide 
{
        anchors.fill: parent

        Image {
            id: background12
            source: "pt/12.jpg"
            anchors.fill: parent
        
    }
}   
    
}
