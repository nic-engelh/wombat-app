from flask import Flask, render_template, request

# Define the tables as dictionaries
puncture_table = {
    '01-05': {'A': 'Glancing blow. No extra damage. +0 hit.', 'B': ' +1 hit.', 'C': ' +2 hits.', 'D': ' +3 hits.', 'E': ' +3 hits.'},
    '06-10': {'A': ' +2 hits.', 'B': ' +3 hits.', 'C': ' +4 hits.', 'D': ' +4 hits.', 'E': 'Unbalance foe with a nice grazing strike. You gain initiative +5 hits.'},
    '11-15': {'A': 'You receive initiative for next round. +4 hit.', 'B': 'Glancing blow to side. +5 hits. You receive initiative next round.', 'C': 'Blow to foe\'s side. +5 hits. You receive initiative next round.', 'D': ' +2 hits. Foe must parry next round.', 'E': ' +3 hits. Foe must parry next round.'},
    '16-20': {'A': ' Foe must parry next round. +4 hits.', 'B': ' Blow to foe. +2 hits. Blow across side. Foe must parry next round at -10.', 'C': 'Blow across side. Foe must parry next round at -20. +3 hits.', 'D': ' Minor side wound. Foe fights at -10. You have the initiative next round.', 'E': ' Stun foe for 1 round. Add +20 to your next attack.'},
    '21-25': {'A': ' Foe must parry next round. +5 hits. Add +10 to your next attack.', 'B': ' Foe must parry next round at -20. +5 hits.', 'C': 'You wound foe along side of hip. Foe is stunned 1 round and takes 1 hit per round.', 'D': ' Foe is stunned 1 round and takes 1 hit per round.', 'E': ' You wound foe along side of hip. Foe is stunned 1 round and takes 1 hit per round.'},
    '26-30': {'A': ' Minor calf wound. Foe takes 1 hit per round.', 'B': ' Minor calf wound. Foe takes 1 hit per round. +2 hits.', 'C': 'Minor calf wound. Foe takes 1 hit per round. Foe takes 2 hits per round.', 'D': ' Minor thigh wound. Foe takes 1 hit per round.', 'E': ' Minor thigh wound. Foe takes 1 hit per round.'},
    '31-35': {'A': ' Strike along foe\'s back. Foe is stunned 1 round and takes 1 hit per round.', 'B': ' Strike along foe\'s back. Foe is stunned 1 round and takes 1 hit per round.', 'C': 'Strike along foe\'s back. Foe is stunned 1 round. Foe takes 1 hit per round.', 'D': ' Strike to foe\'s lower back. Foe is stunned and unable to parry next round.', 'E': ' Strike to foe\'s lower back. Foe is stunned and unable to parry next round.'},
    '36-40': {'A': ' Foe must parry next round at -30.', 'B': ' Minor chest wound. Foe is stunned 1 round. +5 hits. Foe takes 1 hit per round.', 'C': ' Minor chest wound. Foe takes 1 hit per round. +5 hits. Foe is stunned 1 round.', 'D': ' Hard blow to chest. +5 hits. Foe is stunned 1 round.', 'E': ' Blow to chest. +10 hits. Foe has broken rib. Foe is stunned 1 round.'},
    '41-45': {'A': ' Foe must parry next round at -30. +5 hits.', 'B': ' Blow to foe\'s chest. +5 hits. Foe is stunned 1 round.', 'C': ' Hard blow to chest. +5 hits. Foe is stunned 1 round.', 'D': ' Blow to foe\'s chest. +5 hits. Foe is stunned 1 round.', 'E': ' Blow to chest. +10 hits. Foe has broken rib. Foe is stunned 1 round.'},
    '46-50': {'A': ' Strike to foe\'s chest. Foe is stunned 1 round. +5 hits.', 'B': ' Minor chest wound. Foe takes 1 hit per round. +5 hits. Foe is stunned 1 round.', 'C': ' Minor chest wound. Foe takes 1 hit per round. +5 hits. Foe is stunned 1 round.', 'D': ' Strike to foe\'s chest. +5 hits. Foe is stunned 1 round.', 'E': ' Strike to foe\'s chest. +5 hits. Foe is stunned 1 round.'},
    '51-55': {'A': ' Strike to foe\'s chest. Foe is stunned 1 round. +5 hits.', 'B': ' Minor thigh wound. Foe takes 1 hit per round. +5 hits. Foe is stunned 1 round.', 'C': ' Minor thigh wound. Foe takes 1 hit per round. +5 hits. Foe is stunned 1 round.', 'D': ' Strike to foe\'s thigh. Foe is stunned 1 round. +5 hits. Foe takes 1 hit per round.', 'E': ' Strike to foe\'s thigh. Foe is stunned 1 round. +5 hits. Foe takes 1 hit per round.'},
    '56-60': {'A': ' Minor thigh wound. Foe takes 1 hit per round. +5 hits. Foe is stunned 1 round.', 'B': ' Minor thigh wound. Foe takes 1 hit per round. +5 hits. Foe is stunned 1 round.', 'C': ' Strike to foe\'s thigh. Foe is stunned 1 round. +5 hits. Foe takes 1 hit per round.', 'D': ' Strike to foe\'s thigh. Foe is stunned 1 round. +5 hits. Foe takes 1 hit per round.', 'E': ' Strike to foe\'s thigh. Foe takes 5 hits per round. +6 hits. Foe is stunned and unable to parry next round.'},
    '61-65': {'A': ' Minor forearm wound. Foe is stunned next round. +3 hits.', 'B': ' Minor forearm wound. Foe is stunned next round. +3 hits.', 'C': ' Forearm wound. Foe takes 1 hit per round. +3 hits.', 'D': ' Forearm wound and +10 hits. Foe is stunned next round.', 'E': ' Forearm wound. Foe is stunned for 1 round. +3 hits. Foe is stunned for 1 rounds.'},
    '66': {'A': ' Strike to foe\'s shoulder. Arm is useless. Foe is stunned 1 round. +3 hits.', 'B': ' Strike to foe\'s shoulder. Arm is useless. Foe is stunned 1 round. +3 hits.', 'C': ' Strike to foe\'s shoulder. Arm is useless. Foe is stunned 1 round. +3 hits.', 'D': ' Strike to foe\'s shoulder. Arm is useless. Foe is stunned 1 round. +3 hits.', 'E': ' Strike to foe\'s shoulder. Arm is useless. Foe is stunned 1 round. +3 hits.'},
    '67-70': {'A': ' Strike along foe\'s neck. Foe is stunned 1 round. +3 hits. Foe is stunned for 1 round.', 'B': ' Strike to foe\'s neck. Foe is stunned 1 round. +3 hits. Foe is stunned for 1 round.', 'C': ' Strike to foe\'s neck. Foe is stunned 1 round. +3 hits. Foe is stunned for 1 round.', 'D': ' Strike to foe\'s shoulder. Arm is useless. Foe is stunned 1 round. +3 hits.', 'E': ' Blow to foe\'s shoulder. Arm is useless. Foe is stunned 1 round. +3 hits.'},
    '100': {'A': 'Strike through foe\'s back. Foe is stunned 1 round. +3 hits. Foe is stunned for 1 round.', 'B': ' Strike to foe\'s neck. Foe is stunned 1 round. +3 hits. Foe is stunned for 1 round.', 'C': ' Strike through both lungs. Foe drops and is dead in 3 rounds.', 'D': ' Strike through heart. Foe dies instantly.', 'E': ' Strike through brain. Foe dies instantly. Add +20 to your next attack.'}
}

krush_critical_strike_table = {
    '01-05': {'A': 'Zip.', 'B': 'Weak grip. No extra damage.', 'C': '+1 hit.', 'D': '+2 hits.', 'E': '+3 hits.'},
    '06-10': {'A': '+1 hit.', 'B': '+2 hits.', 'C': '+2 hits.', 'D': '+4 hits.', 'E': 'Glancing blow +6 hits. Foe is stunned and unable to parry next round. You have the initiative next round.'},
    '11-15': {'A': 'Glancing blow. Foe takes 1 hit. You have the initiative next round.', 'B': 'Glancing blow. +3 hits. You have the initiative next round.', 'C': "Blow to foe's side. +5 hits. You receive initiative next round.", 'D': '+5 hits. Foe must parry next round at -10.', 'E': '+6 hits. Foe is stunned for 1 round. Add +10 to your next swing.'},
    '16-20': {'A': '+2 hits. Foe must parry next round at +10.', 'B': "Blow to foe's side. +4 hits. Foe must parry next round at -10.", 'C': "Blow to foe's side. +5 hits. Foe must parry next round at -20.", 'D': 'Minor fracture of ribs. +3 hits. Foe fights at -10. You have initiative next round.', 'E': 'Strong blow. Foe is stunned and unable to parry next round. Add +10 to your next swing.'},
    '21-35': {'A': 'Foe must parry next round. +3 hits. Add +5 to your next swing.', 'B': 'Foe must parry next round at -20. +4 hits.', 'C': "You break foe's rib. +3 hits. Foe is stunned during next round. Initiative is yours also.", 'D': "Strike to Foe's side. +4 hits. Foe is stunned and unable to parry during next round.", 'E': "Strike cracks foe's ribs. +6 hits. Foe is at -10. You have initiative next round."},
    '36-45': {'A': "Bruise foe's calf. +5 hits. You gain the initiative. Foe fights at -10 for next 2 rounds.", 'B': "Bruise foe's calf. +6 hits. You gain the initiative. Foe fights at -20 for next 2 rounds.", 'C': "Bruise foe's calf. +9 hits. You gain the initiative. Foe fights at -25 for next 3 rounds.", 'D': 'Major calf bruise. +10 hits. Foe fights at -30. You have the initiative next round.', 'E': 'Strike to upper leg. Minor fracture. +12 hits. Foe fights at -40. +15 to your next swing. Initiative is yours.'},
    '46-50': {'A': "Blow to foe's back. +4 hits. Foe must parry next round at -15. +10 to your next swing.", 'B': "Blow to foe's back. +6 hits. Foe must parry next round at -25.", 'C': 'Blow to back. +5 hits. Stunned and unable to parry 1 rnd. You have the initiative next round.', 'D': 'Hard blow to back. +10 hits. Foe is stunned and unable to parry during next round.', 'E': "Strike to foe's lower back. You break foe's back. +12 hits. Foe is stunned and unable to parry for next 2 rounds."},
    '51-55': {'A': "Blow to foe's chest. +5 hits. Foe must parry next round at -25. Foe has a bruised rib.", 'B': "Blow to foe's chest. +6 hits. Foe must parry for next 2 rounds.", 'C': "Hard blow to chest. +8 hits. Foe fights at -10. Foe is stunned during next round.", 'D': "Blow to Foe's chest. +12 hits. Foe has a pair of broken ribs and must fight at -15.", 'E': 'Foe is stunned for 2 rounds. Foe fights -15.'},
    '56-60': {'A': "Strike cracks foe's thigh. +6 hits. Foe is forced to parry next round at -25. Glancing blow.", 'B': "Strike cracks foe's thigh. +8 hits. Foe has a bruise and is forced to parry for 1 round. Foe is at -5.", 'C': "Strike cracks foe's thigh. +8 hits. Foe is at -5. Add +10 to your next swing. Foe is stunned during next round.", 'D': 'Blow to thigh. Foe is stunned next round. +6 hits. Foe is at -10 and is upset.', 'E': 'Blow to thigh. Foe is dropped and unable to parry next round. Foe is at -10. +10 hits.'},
    '61-65': {'A': "Blow to foe's forearm. Stunned. +5 hits. Foe is at -10. Add +20 to your next swing.", 'B': "Blow to foe's forearm. Foe is at -10. +6 hits. Foe is stunned during next round.", 'C': "Blow to foe's forearm. Foe is stunned during next round and unable to parry. Add +10 to your next swing.", 'D': 'Blow to forearm. Foe is stunned during next round and must fight at -15. +10 hits. Foe is at -10.', 'E': "Blow to forearm. Foe drops weapon. +12 hits. Foe is stunned for next round."},
    '66': {'A': "Shatter shoulder in foe's weapon arm. Foe is at -30 for 1 round. +8 hits. Foe is stunned for 2 rounds. +8 hits.", 'B': "Shatter elbow in foe's weapon arm. +10 hits. Foe drops weapon, and is stunned.", 'C': "Shatter foe's knee. +9 hits. Foe is knocked down, drops weapon and is unable to parry for 3 rounds. Foe at -50.", 'D': "Blow to side of foe's head. If foe has no helm he is killed. If he has a helm, you knock him out for 4 hours. +20 hits.", 'E': 'Blow to side of neck, crushes esophagus. Foe dies in agony. +15 hits. Add +15 to your next swing.'},
    '67-70': {'A': 'Strike upper chest area. Bruises. Foe is stunned for 3 rounds and unable to parry during next round.', 'B': 'Strike upper chest area. Foe is stunned for 2 rounds and unable to parry for 2 rounds +10 hits. Foe is at -10.', 'C': 'Strike upper chest area. Foe is stunned and unable to parry for 2 rounds. +10 hits. Foe is at -10.', 'D': "Blow to foe's shoulder area. Minor fracture. Foe is at -20. Foe is stunned and unable to parry for 2 rounds.", 'E': "Blow to foe's shield shoulder. If foe has a shield, it is broken. Foe drops the shield, the shoulder is shattered. Foe is stunned."},
    '71-75': {'A': "Blow to foe's upper leg. Bad bruise. +5 hits. Foe is stunned for 2 rounds and unable to parry for 2 rounds. Foe is at -20.", 'B': "Blow to foe's calf. Foe is at -35. +10 hits. Foe is stunned for next round and unable to parry next round.", 'C': "Blow to foe's calf. Foe is stunned and unable to parry. +10 hits. Foe is at -40.", 'D': "Blow to foe's knee cap. Foe breaks a bone in leg. Foe is at -40. +12 hits. Foe is stunned and unable to parry for 2 rounds. Major cartilage damage.", 'E': "Foe breaks foe's leg. Foe is at -50. Foe is stunned and unable to parry for 3 rounds. +15 hits."},
    '76-80': {'A': "Blow to foe's shield arm. If foe has a shield, it is broken. Foe's arm is stunned and arm is badly broken and useless.", 'B': "Blow to foe's shield arm, shatters wrist. Arm is useless. Foe is stunned for next round. +6 hits.", 'C': "Blow to foe's weapon arm. Bad bruise. +9 hits. Foe is stunned and unable to parry for 2 rnds. Foe is at -30.", 'D': "Blow to foe's weapon arm. Foe is stunned and unable to parry for 2 rounds. Foe is at -30. +8 hits. Tendon damage.", 'E': "Blow to foe's elbow. +9 hits. Joint is shattered. Arm is useless. Foe is stunned and unable to parry for 2 rounds."},
    '81-85': {'A': "Blow to foe's side. +10 hits. Foe is stunned and unable to parry for 2 rounds. Foe is at -20.", 'B': "Blow to foe's side. +12 hits. Foe has a broken rib. Foe is stunned and unable to parry for 2 rounds. Foe is at -30.", 'C': "Strike in foe's side. Breaks two ribs. Foe is at -35. +10 hits. Foe is stunned and unable to parry for 2 rounds.", 'D': 'Major blow to side of foe. Foe is stunned and unable to parry next round. Foe is stunned and unable to parry for 2 rounds.', 'E': 'Catch foe in armpit. +10 hits. Crush ribs. Foe dies in 2 rounds. Foe drops and dies of nerve and organ damage. Foe is down.'},
    '86-90': {'A': "Blow to foe's back. +12 hits. Muscle and cartilage. Foe is stunned and unable to parry for 3 rounds. Foe is at -25.", 'B': 'Strike to back knocks foe down and smashes tendons. Foe is stunned and unable to parry for 4 rounds. Foe is at -30.', 'C': 'Strike to back smashes muscle and breaks bone. +20 hits. Foe is at -50. Foe is knocked down and stunned for 6 rounds.', 'D': 'Blow to neck on back breaks backbone and destroys spine. +20 hits. Foe falls and dies in 2 rounds.', 'E': 'Strike neck from below and severs an artery. Foe cannot breath and dies in 12 rounds. The poor sod then chokes.'},
    '91-95': {'A': "Break foe's nose. Foe is stunned and unable to parry for 2 rnds. +15 hits. Foe fights at -30 for 2 days.", 'B': "Foe's upper head hit. If no helm, foe dies from a concussion in 3 weeks. If he has helm, 12 hits and foe is stunned for 12 rnds.", 'C': 'Foe shatters thigh. +9 hits and a compound fracture. Foe is stunned and at -75. Foe dies after 12 rounds of inactivity.', 'D': 'Blow shatters shield arm. Bone severs nerve and an artery. Foe dies in 3 hours and is at -25 after 9 inactive rounds.', 'E': "Blast to foe's back. +25 hits. Bone is driven into vital organs and foe is down for 3 rounds. Then dies."},
    '96-99': {'A': "Blow to foe's head. If foe has no helm he is dead. If he has a helm, foe is knocked down and stunned 6 rnds. +20 hits.", 'B': "Foe's chest. Send rib cage through heart. Foe drops and dies. Add +20 to your next swing.", 'C': "Foe's abdomen destroys a variety of organs. The poor slob is down and out. +20 hits. Foe is incapacitated.", 'D': "Blow cracks foe's side crushes chest cavity. Foe drops and dies in agony. Add +25 to your next swing.", 'E': "Crush foe's skull. +30 hits. Opponent dies immediately. Add +20 to your next swing. You have a half round left to act."},
    '100': {'A': "Blow through foe's jaw. Drives bone through brain. Foe dies. Add +20 to your next swing.", 'B': "Blow to back of neck paralyzes foe from the shoulders down. +25 hits. Foe is quite stunned.", 'C': "Strike to forehead. +25 hits. Foe's eyes destroy and destroy brain. Foe is stunned and unable to parry 21 rounds.", 'D': "Strike to foe's chest area. Destroy foe's heart. Foe dies immediately. +25 hits. Foe's dead.", 'E': "Strike in foe's hip. Opponent is stunned for 2 rounds, active defense is at -35. +35 hits. Foe dies of nerve damage."}
}

slash_table = {
    '01-05': {'A': 'Zip.', 'B': 'Weak strike. +0 hits.', 'C': ' +1 hit.', 'D': ' +2 hits.', 'E': ' +3 hits. Unbalance foe. +5 hits. You receive initiative next round.'},
    '06-10': {'A': ' +1 hit.', 'B': ' +2 hits.', 'C': ' +3 hits.', 'D': ' +4 hits.', 'E': 'Glancing blow to side. +5 hits. You receive initiative next round.'},
    '11-15': {'A': 'Glancing blow. +2 hits. You receive initiative next round.', 'B': 'Glancing blow to side. +3 hits. You receive initiative next round.', 'C': 'Blow to foe\'s side. +5 hits. You receive initiative next round.', 'D': 'Minor side wound. +2 hits. Foe must parry next round.', 'E': 'Minor side wound. +3 hits. Foe must parry next round at -10.'},
    '16-20': {'A': ' +2 hits. Foe must parry next round.', 'B': 'Blow to foe\'s side. +3 hits. Foe must parry next round at -10.', 'C': 'Blow to foe\'s side. +4 hits. Foe must parry next round at -20.', 'D': 'Minor wound to side. +5 hits. Foe fights at -10. You have initiative next round.', 'E': 'Stun foe for 1 round. +5 hits. Add +10 to your next swing.'},
    '21-35': {'A': 'Foe must parry next round. +3 hits. Add +5 to your next swing.', 'B': 'Foe must parry next round at -20. +4 hits.', 'C': 'You cut foe\'s side. +3 hits. Foe is stunned during next round.', 'D': 'Strike to foe\'s side. +4 hits. Foe is stunned and unable to parry during next round.', 'E': 'Strike cuts foe\'s ribs. +6 hits. Foe is at -10. You have initiative next round.'},
    '36-45': {'A': 'Cut foe\'s calf. +5 hits. You gain the initiative. Foe fights at -10 for next 2 rounds.', 'B': 'Cut foe\'s calf. +6 hits. You gain the initiative. Foe fights at -20 for next 2 rounds.', 'C': 'Cut foe\'s calf. +9 hits. You gain the initiative. Foe fights at -25 for next 3 rounds.', 'D': 'Major calf cut. +10 hits. Foe fights at -30. You have the initiative next round.', 'E': 'Strike to upper leg. Minor cut. +12 hits. Foe fights at -40. +15 to your next swing. Initiative is yours.'},
    '46-50': {'A': 'Blow to foe\'s back. +4 hits. Foe must parry next round at -15. +10 to your next swing.', 'B': 'Blow to foe\'s back. +6 hits. Foe must parry next round at -25.', 'C': 'Blow to back. +5 hits. Stunned and unable to parry 1 rnd. You have the initiative next round.', 'D': 'Hard blow to back. +10 hits. Foe is stunned and unable to parry during next round.', 'E': 'Strike to foe\'s lower back. You cut foe\'s back. +12 hits. Foe is stunned and unable to parry for next 2 rounds.'},
    '51-55': {'A': 'Blow to foe\'s chest. +5 hits. Foe must parry next round at -25. Foe has a cut rib.', 'B': 'Blow to foe\'s chest. +6 hits. Foe must parry for next 2 rounds.', 'C': 'Hard blow to chest. +8 hits. Foe fights at -10. Foe is stunned during next round.', 'D': 'Blow to foe\'s chest. +12 hits. Foe has a pair of cut ribs and must fight at -15.', 'E': 'Foe is stunned for 2 rounds. Foe fights -15.'},
    '56-60': {'A': 'Strike cuts foe\'s thigh. +6 hits. Foe is forced to parry next round at -25. Glancing blow.', 'B': 'Strike cuts foe\'s thigh. +8 hits. Foe has a cut and is forced to parry for 1 round. Foe is at -5.', 'C': 'Strike cuts foe\'s thigh. +8 hits. Foe is at -5. Add +10 to your next swing. Foe is stunned during next round.', 'D': 'Blow to thigh. Foe is stunned next round. +6 hits. Foe is at -10 and is upset.', 'E': 'Blow to thigh. Foe is dropped and unable to parry next round. Foe is at -10. +10 hits.'},
    '61-65': {'A': 'Blow to foe\'s forearm. Stunned. +5 hits. Foe is at -10. Add +20 to your next swing.', 'B': 'Blow to foe\'s forearm. Foe is at -10. +6 hits. Foe is stunned during next round.', 'C': 'Blow to foe\'s forearm. Foe is stunned during next round and unable to parry. Add +10 to your next swing.', 'D': 'Blow to forearm. Foe is stunned during next round and must fight at -15. +10 hits. Foe is at -10.', 'E': 'Blow to forearm. Foe drops weapon. +12 hits. Foe is stunned for next round.'},
    '66': {'A': 'Cut shoulder in foe\'s weapon arm. Foe is at -30 for 1 round. +8 hits. Foe is stunned for 2 rounds. +8 hits.', 'B': 'Cut elbow in foe\'s weapon arm. +10 hits. Foe drops weapon, and is stunned.', 'C': 'Cut foe\'s knee. +9 hits. Foe is knocked down, drops weapon and is unable to parry for 3 rounds. Foe at -50.', 'D': 'Blow to side of foe\'s head. If foe has no helm he is killed. If he has a helm, you knock him out for 4 hours. +20 hits.', 'E': 'Blow to side of neck, cuts esophagus. Foe dies in agony. +15 hits. Add +15 to your next swing.'},
    '67-70': {'A': 'Strike upper chest area. Cuts. Foe is stunned for 3 rounds and unable to parry during next round.', 'B': 'Strike upper chest area. Foe is stunned for 2 rounds and unable to parry for 2 rounds +10 hits. Foe is at -10.', 'C': 'Strike upper chest area. Foe is stunned and unable to parry for 2 rounds. +10 hits. Foe is at -10.', 'D': 'Blow to foe\'s shoulder area. Minor cut. Foe is at -20. Foe is stunned and unable to parry for 2 rounds.', 'E': 'Blow to foe\'s shield shoulder. If foe has a shield, it is broken. Foe drops the shield, the shoulder is cut. Foe is stunned.'},
    '71-75': {'A': 'Blow to foe\'s upper leg. Bad cut. +5 hits. Foe is stunned for 2 rounds and unable to parry for 2 rounds. Foe is at -20.', 'B': 'Blow to foe\'s calf. Foe is at -35. +10 hits. Foe is stunned for next round and unable to parry next round.', 'C': 'Blow to foe\'s calf. Foe is stunned and unable to parry. +10 hits. Foe is at -40.', 'D': 'Blow to foe\'s knee cap. Foe cuts a bone in leg. Foe is at -40. +12 hits. Foe is stunned and unable to parry for 2 rounds. Major cartilage damage.', 'E': 'Foe cuts foe\'s leg. Foe is at -50. Foe is stunned and unable to parry for 3 rounds. +15 hits.'},
    '76-80': {'A': 'Blow to foe\'s shield arm. If foe has a shield, it is broken. Foe\'s arm is stunned and arm is badly cut and useless.', 'B': 'Blow to foe\'s shield arm, cuts wrist. Arm is useless. Foe is stunned for next round. +6 hits.', 'C': 'Blow to foe\'s weapon arm. Bad cut. +9 hits. Foe is stunned and unable to parry for 2 rnds. Foe is at -30.', 'D': 'Blow to foe\'s weapon arm. Foe is stunned and unable to parry for 2 rounds. Foe is at -30. +8 hits. Tendon damage.', 'E': 'Blow to foe\'s elbow. +9 hits. Joint is cut. Arm is useless. Foe is stunned and unable to parry for 2 rounds.'},
    '81-85': {'A': 'Blow to foe\'s side. +10 hits. Foe is stunned and unable to parry for 2 rounds. Foe is at -20.', 'B': 'Blow to foe\'s side. +12 hits. Foe has a cut rib. Foe is stunned and unable to parry for 2 rounds. Foe is at -30.', 'C': 'Strike in foe\'s side. Cuts two ribs. Foe is at -35. +10 hits. Foe is stunned and unable to parry for 2 rounds.', 'D': 'Major blow to side of foe. Foe is stunned and unable to parry next round. Foe is stunned and unable to parry for 2 rounds.', 'E': 'Catch foe in armpit. +10 hits. Cut ribs. Foe dies in 2 rounds. Foe drops and dies of nerve and organ damage. Foe is down.'},
    '86-90': {'A': 'Blow to foe\'s back. +12 hits. Muscle and cartilage. Foe is stunned and unable to parry for 3 rounds. Foe is at -25.', 'B': 'Strike to back knocks foe down and cuts tendons. Foe is stunned and unable to parry for 4 rounds. Foe is at -30.', 'C': 'Strike to back cuts muscle and breaks bone. +20 hits. Foe is at -50. Foe is knocked down and stunned for 6 rounds.', 'D': 'Blow to neck on back cuts backbone and destroys spine. +20 hits. Foe falls and dies in 2 rounds.', 'E': 'Strike neck from below and severs an artery. Foe cannot breath and dies in 12 rounds. The poor sod then chokes.'},
    '91-95': {'A': 'Cut foe\'s nose. Foe is stunned and unable to parry for 2 rnds. +15 hits. Foe fights at -30 for 2 days.', 'B': 'Foe\'s upper head hit. If no helm, foe dies from a cut in 3 weeks. If he has helm, 12 hits and foe is stunned for 12 rnds.', 'C': 'Foe cuts thigh. +9 hits and a cut fracture. Foe is stunned and at -75. Foe dies after 12 rounds of inactivity.', 'D': 'Blow cuts shield arm. Bone severs nerve and an artery. Foe dies in 3 hours and is at -25 after 9 inactive rounds.', 'E': 'Blast to foe\'s back. +25 hits. Bone is driven into vital organs and foe is down for 3 rounds. Then dies.'},
    '96-99': {'A': 'Blow to foe\'s head. If foe has no helm he is dead. If he has a helm, foe is knocked down and stunned 6 rnds. +20 hits.', 'B': 'Foe\'s chest. Send rib cage through heart. Foe drops and dies. Add +20 to your next swing.', 'C': 'Foe\'s abdomen destroys a variety of organs. The poor slob is down and out. +20 hits. Foe is incapacitated.', 'D': 'Blow cuts foe\'s side crushes chest cavity. Foe drops and dies in agony. Add +25 to your next swing.', 'E': 'Cut foe\'s skull. +30 hits. Opponent dies immediately. Add +20 to your next swing. You have a half round left to act.'},
    '100': {'A': 'Blow through foe\'s jaw. Drives bone through brain. Foe dies. Add +20 to your next swing.', 'B': 'Blow to back of neck paralyzes foe from the shoulders down. +25 hits. Foe is quite stunned.', 'C': 'Strike to forehead. +25 hits. Foe\'s eyes destroy and destroy brain. Foe is stunned and unable to parry 21 rounds.', 'D': 'Strike to foe\'s chest area. Destroy foe\'s heart. Foe dies immediately. +25 hits. Foe\'s dead.', 'E': 'Strike in foe\'s hip. Opponent is stunned for 2 rounds, active defense is at -35. +35 hits. Foe dies of nerve damage.'}
}

tables = {'puncture': puncture_table, 'crush': krush_critical_strike_table, 'slash': slash_table}

threat_ranges = {
    'a': {'A': 6, 'B': 8, 'C': 10, 'D': 12, 'E': 14, 'F': 16, 'G': 18},  # 20 for x2 damage
    'b': {'A': 5, 'B': 7, 'C': 9, 'D': 11, 'E': 13, 'F': 15, 'G': 17},  # 19-20 or 20 for x3/x4 damage
    'c': {'A': 4, 'B': 6, 'C': 8, 'D': 10, 'E': 12, 'F': 14, 'G': 16},  # 18-20
    'd': {'A': 3, 'B': 5, 'C': 7, 'D': 9, 'E': 11, 'F': 13, 'G': 15},   # 15-20
    'e': {'A': 10, 'B': 12, 'C': 14, 'D': 16, 'E': 18, 'F': 20, 'G': 22}  # Grapple, Overrun, Bull-rush, Trip, etc.
}

def get_column(difference, threat_range):
    if threat_range not in threat_ranges:
        raise ValueError("Invalid threat range. Choose 'a', 'b', 'c', 'd', or 'e'.")
    thresholds = threat_ranges[threat_range]
    if difference < thresholds['A']:
        return 'A'
    elif difference < thresholds['B']:
        return 'B'
    elif difference < thresholds['C']:
        return 'C'
    elif difference < thresholds['D']:
        return 'D'
    elif difference < thresholds['E']:
        return 'E'
    elif difference < thresholds['F']:
        return 'F'
    else:
        return 'G'

def get_row(roll):
    if not 1 <= roll <= 100:
        raise ValueError("Roll must be between 1 and 100.")
    if roll <= 5: return '01-05'
    elif roll <= 10: return '06-10'
    elif roll <= 15: return '11-15'
    elif roll <= 20: return '16-20'
    elif roll <= 25: return '21-25'
    elif roll <= 30: return '26-30'
    elif roll <= 35: return '31-35'
    elif roll <= 40: return '36-40'
    elif roll <= 45: return '41-45'
    elif roll <= 50: return '46-50'
    elif roll <= 55: return '51-55'
    elif roll <= 60: return '56-60'
    elif roll <= 65: return '61-65'
    elif roll == 66: return '66'
    elif roll <= 70: return '67-70'
    elif roll <= 75: return '71-75'
    elif roll <= 80: return '76-80'
    elif roll <= 85: return '81-85'
    elif roll <= 90: return '86-90'
    elif roll <= 95: return '91-95'
    elif roll <= 99: return '96-99'
    else: return '100'

def get_critical(damage_type, difference, roll, threat_range):
    column = get_column(difference, threat_range)
    row = get_row(roll)
    table = tables.get(damage_type.lower())
    if not table:
        raise ValueError("Invalid damage type. Choose 'puncture', 'crush', or 'slash'.")
    row_data = table.get(row)
    if not row_data:
        raise ValueError("Invalid row for roll.")
    return row_data.get(column, "No effect.")

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    error = None
    if request.method == 'POST':
        damage_type = request.form['damage_type']
        threat_range = request.form['threat_range']
        try:
            difference = int(request.form['difference'])
            roll = int(request.form['roll'])
            result = get_critical(damage_type, difference, roll, threat_range)
            row = get_row(roll)
            column = get_column(difference, threat_range)
        except ValueError as e:
            error = str(e)
    return render_template('index.html', result=result, error=error)

if __name__ == '__main__':
    app.run(debug=True)