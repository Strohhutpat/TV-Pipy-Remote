# TV-Pipy-Remote
Control your  course-information-screen by Raspberry Pi
TV-Pipy-Remote v0.9

German:
Unsere Kursmonitore , basierend auf einem einfach LCD (32") TV + Raspberry Pi 3, 
zeigen per Chromium unsere Tageskurse in der jeweiligen Geschäftstelle an.
Dieses selbst entwickelte, KIRAA genannte, Programm basiert auf PHP und MSSQLSRV.

Um die Screens zeitlich steuern zu können (auch bei seltenen Wochenend-Kursen und bei Tagen ohne Kurse, aber mit Werbung),
lesen wir die jeweiligen Geschäftsstellen-Kurse live per PHP+XML aus und 
das TV-Pipy-Remote Script schaltet damit die Fernseher an bzw. aus.

Manche TV´s können kein CEC bzw. nur Teilweise (kein Standby-Command), siehe hierzu
http://kodi.wiki/view/CEC#Manufacturer_Support
