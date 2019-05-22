# ManuscriptManager
Create an mp3 file from a text file (manuscript) containing roles, dialogues, parenthesis and voices.

Commands:
  ROLE     - creates a role element with own voice
  SOUND    - creates a sound element from mp3 files(s) or other sounds
  WAIT     - creates a wait element
  GROUP    - creates a group element of roles that speaks at same time
  SETTINGS - sets overall settings, eg.
             -- export parameters
             -- debug commands
             -- text processing
  a role element  - speaks text or creates a sound element
  a sound element - plays the sound
  a wait element  - waits a specific time
  a group element - the roles of the group speak the text or create a sound 
