'''IOR Task Version 3.3.1 (Agathe)

RAPPEL : lignes à vérifier, repérées par ###

Modifications mineures :
    - écran inter-bloc autonomisé, pendant l'entraînement (le sujet passe quand il veut au bloc d'entraînement suivant)
'''

from expyriment import design, control, stimuli, io, misc
import tkinter
import os
from leepfun import *
# Set develop mode, instead of full-length experiment
dev = False ###

# Initialize and start experiment
exp = design.Experiment("IOR Task")
control.initialize(exp)
control.start(skip_ready_screen=True,subject_id=ipsubject()) #  get subject number between 1 and 20 from IP address

# Set parameters
    # inter-subject parameters
exp_type = 1  ### 1 for type 1 (speed), 0 pour type 2 (motor mapping)
is_square_up = True
is_AP_first = ((exp.subject // 2) % 2)  # type bool (relevant for exp_type = 0)
is_slow_first = ((exp.subject // 2) % 2)  # type bool (relevant for exp_type = 1)
is_square_right = (exp.subject % 2 == 0)  # type bool 
e0, e1, e2 = 0, 1, 2
if (exp.subject // 4) % 2:
    eccentricity_order = [e0, e1, e2] if exp.subject % 2 else [e0, e2, e1]
else:
    eccentricity_order = [e1, e0, e2] if exp.subject % 2 else [e1, e2, e0]

    # geometric parameters
root = tkinter.Tk()
width, height = root.winfo_screenmmwidth()/10 , root.winfo_screenmmheight()/10
screen_size = (width, height)
d_toscreen = 75
r_large = 5
width_large = 2
r_small = 2
r_circle = 25
l_square = 50
r_memo = 15
l_memo = 30
d_memo = 200 if exp.screen.window_mode else 400

    # time parameters
block_lengths = [3, 10] if dev else [25, 240]
display_time = 200
f_minipause = [3, 5] if dev else [25, 120] # condition : f_minipause[i] doit diviser block_lengths[i]
series_perblock = [block_lengths[i] // f_minipause[i] for i in range(2)]
t_minipause = [0, 3000] if dev else [0, 10000]
t_interblock = [3000, 10000] if dev else [10000, 60000]
t_beginning = 500
t_feedback = 3000 if dev else 5000

    # user parameters
pass_key = misc.constants.K_RETURN
end_key = misc.constants.K_EXCLAIM

    # block parameters
A, P, G, D = misc.constants.K_a if os.name!='nt' else misc.constants.K_q, misc.constants.K_p, misc.constants.K_LEFT, misc.constants.K_RIGHT
motricities = [[G, D], [A, P]]
key_string = {A: "A", P: "P", G: "←", D: "→", pass_key: "Entrée"}
def is_right(key):
    if key in [P,D]:
        return True
    if key in [A, G]:
        return False
    return None
angles = [0, 3, 7]
eccentricities = list(map(lambda a: misc.geometry.visual_angle2position((0,2*a), d_toscreen, 
                                                                        screen_size)[1]/2, 
                          angles))
delays = [700, 1200]

    # clock generation
temps_rouge = [0]*(1+block_lengths[1])
temps_bleu = [0]*(1+block_lengths[1])
t_b , t_r = 0 , 0
for i in range (1,1+block_lengths[1]) :
    if i%2 == 1 :
        t_b += display_time
        t_r += display_time
    else :
        t_b += delays[1]
        t_r += delays[0]
    temps_bleu[i] , temps_rouge[i] = t_b , t_r
temps = [temps_rouge, temps_bleu]

    # block ordering
motricity_order = [1, 1] if exp_type else ([1, 0] if is_AP_first else [0, 1])
delay_order = [0, 0] if exp_type==0 else ([1, 0] if is_slow_first else [0, 1])

    # data parameters
exp.data_variable_names = ["BlockId", "SerieId", "TrialId", "Motricity", "Eccentricity", "Delay", 
                           "Stimulus", "Repetition", "Button", "Answer", "Correct", "RT",
                           "StimulusOnset", "IsMultiKeyPress", "AddKeysWhat", "AddKeysWhen",
                           "IsPause"]

    # reward function
def reward(r):
    """ 
    reward(r) returns the bonus, which is a (step-wise) linear function of the error r (in %).
    Bonus increase with performance. It is at most +2.5€, 0€ for r=7% clipped to -10€. The bonus
    changes with 0.5€ steps.
    """
    return max(-10, round(2*(-33.2 + (100-r)*2.5/7))/2)
# import matplotlib.pyplot as plt
# plt.plot(r, [reward(r_) for r_ in r])

# Set and preload stimuli
    # define fixcross
fixcross = stimuli.Circle(r_large, colour=misc.constants.C_WHITE, line_width=width_large, 
                          position=None, anti_aliasing=10)
fixcross2 = stimuli.Circle(r_small, colour=misc.constants.C_WHITE, line_width=0, 
                           position=None, anti_aliasing=10)
fixcross2.plot(fixcross)

    # define memo
memo_disque = stimuli.Circle(r_memo, position=[d_memo,-d_memo], 
                             colour=misc.constants.C_DARKGREY, anti_aliasing=10)
memo_carre = stimuli.Rectangle([l_memo, l_memo], position=[-d_memo, -d_memo], 
                               colour=misc.constants.C_DARKGREY, corner_anti_aliasing=10)
if is_square_right:
    memo_disque.reposition((-d_memo, -d_memo)), memo_carre.reposition((d_memo, -d_memo))

    # preload inter-stimulus canvas
inter = stimuli.BlankScreen()
fixcross.plot(inter), memo_disque.plot(inter), memo_carre.plot(inter)
inter.preload()

# Create design
for mode_id in range(2): # 0 pour entraînement, 1 pour expérience
    if mode_id == 0:
        # Use a fixed order, with increasing levels of difficulty, for training
        block_motricity_order = [1, 1, 1, 1, 1, 1] if exp_type else [0, 0, 0, 1, 1, 1]
        block_delay_order = [1, 1, 1, 0, 0, 0] if exp_type else [0, 0, 0, 0, 0, 0]
        block_eccentricity_order = [0, 1, 2, 0, 1, 2]
    else:
        # Use the pre-defined, randomalized order, for data collection
        block_motricity_order = [motricity_order[0]]*3 + [motricity_order[1]]*3
        block_delay_order = [delay_order[0]]*3 + [delay_order[1]]*3
        block_eccentricity_order = eccentricity_order * 2        
        
    for block_id in range(6): # entre 0 et 5
        b = design.Block()

        # set block factors
        b.set_factor("BlockId", block_id)
        b.set_factor("Motricity", block_motricity_order[block_id]) # entre 0 et 1
        b.set_factor("Eccentricity", block_eccentricity_order[block_id]) # entre 0 et 2
        b.set_factor("Delay", block_delay_order[block_id]) # entre 0 et 1

        # get block parameters
        mot = motricities[b.get_factor("Motricity")] # liste de 2 touches
        ecc = eccentricities[b.get_factor("Eccentricity")]
        delay = delays[b.get_factor("Delay")]

        for trial_id in range(block_lengths[mode_id]):
            t = design.Trial()

            # generate random stimulus
            is_square = design.randomize.coin_flip() # type bool

            # set trial factors
            t.set_factor("TrialId", trial_id)
            t.set_factor("Stimulus", is_square)

            # build stimulus canvas
            canvas = stimuli.BlankScreen() # canvas = stimuli + fixcross + memo
            fixcross.plot(canvas)
            
            if is_square:
                s = stimuli.Rectangle([l_square, l_square], 
                                      position=[0, ecc * (1 if is_square_up else -1)], 
                                      colour=misc.constants.C_DARKGREY, corner_anti_aliasing=10) 
            else:
                s = stimuli.Circle(r_circle, 
                                   position=[0, -ecc * (1 if is_square_up else -1)], 
                                   colour=misc.constants.C_DARKGREY, anti_aliasing=10)
                
            if ecc == 0:
                fixcross.plot(s)
            s.plot(canvas)

            memo_disque.plot(canvas) , memo_carre.plot(canvas)
            t.add_stimulus(canvas)

            b.add_trial(t)
        exp.add_block(b)

# Run experiment
    # introduction speech screen
stimuli.TextScreen("Introduction", "Veuillez écouter les consignes de l'expérience.").present()
exp.keyboard.wait(keys=pass_key)


for mode_id in range(2):
    
    X = 0 # compteur d'erreurs totales
    Y = 0 # somme de rt moyens
    Z = 0 # compteur de blocs avec au moins une réponse
    
    for block_id in range(6*mode_id, 6*(mode_id+1)):
        b = exp.blocks[block_id]

        # display instructions
        canvas_instruct = stimuli.BlankScreen()
        text = stimuli.TextScreen("Bloc " + ("" if mode_id else "d'entraînement ") + 
                                  "n°" + str(b.get_factor("BlockId")+1) + " (sur 6)",
                                  "Instructions" + "\n\n" + "Appuyez sur " + 
                                  key_string[motricities[b.get_factor("Motricity")][int(is_square_right)]] + 
                                  " pour carré et sur " + key_string[motricities[b.get_factor("Motricity")][1 - int(is_square_right)]] + 
                                  " pour rond, à l'aide de " + 
                                  ("vos deux mains." if b.get_factor("Motricity") else "deux doigts de votre main droite.") + 
                                  "\n" + 
                                  "N'oubliez pas de maintenir votre regard sur le symbole au centre." "\n\n" + 
                                  ("Le bloc va durer moins de " + ("6" if b.get_factor("Delay") else "4") + " minutes, et sera entrecoupé d'une mini-pause." 
                                   if mode_id else "Le bloc va durer moins d'une minute.") + "\n\n" + 
                                  "Appuyez sur " + key_string[pass_key] + 
                                  " pour démarrer le bloc." +
                                  ("\n\n" + "Paramètres du bloc" + "\n\n" + 
                                   "Motricité : " + key_string[motricities[b.get_factor("Motricity")][0]] + ", " + 
                                   key_string[motricities[b.get_factor("Motricity")][1]] + "\n" + 
                                   "Eccentricité : " + str(eccentricities[b.get_factor("Eccentricity")]) + " pixels" + "\n" + 
                                   "Délai : " + str(delays[b.get_factor("Delay")]) + " ms" if dev else ""))
        memo_carre.plot(canvas_instruct)
        memo_disque.plot(canvas_instruct)
        text.plot(canvas_instruct)
        canvas_instruct.present()
        exp.keyboard.wait(keys=pass_key)

        # set local variables for feedback at the end of the block
        S=0 # somme de rt
        N=0 # compteur de réponses
        E=0 # compteur d'erreurs ou non réponses
        M=0 # compteur de stimuli

        for serie_id in range(series_perblock[mode_id]):
            # before first stimulus screen
            inter.present()
            t0 = exp.clock.time
            while exp.clock.time < t0 + t_beginning :
                pass

            # run trials
            time = [exp.clock.time + x for x in temps[b.get_factor("Delay")]]
            i = 1
            for j in range(serie_id*f_minipause[mode_id],(serie_id+1)*f_minipause[mode_id]) :
                t=b.trials[j]
                t.stimuli[0].present(clear=True)
                stim_onset = exp.clock.time
                button, rt = exp.keyboard.wait(keys=motricities[b.get_factor("Motricity")],
                                               duration=display_time)
                multi_key_press = []
                if j==serie_id*f_minipause[mode_id]:
                    is_Rep=None
                    is_Pause=True
                else:
                    is_Pause=False
                    is_Rep=(t.get_factor("Stimulus")==b.trials[j-1].get_factor("Stimulus"))
                while exp.clock.time < time[i]:
                    new_button, _ = exp.keyboard.wait(keys=motricities[b.get_factor("Motricity")],
                                               duration=time[i]-exp.clock.time)
                    if new_button is not None:
                        multi_key_press.append((new_button, exp.clock.time - stim_onset))
                    pass
                i += 1
                inter.present()
                if rt == None:
                    button, rt = exp.keyboard.wait(keys=motricities[b.get_factor("Motricity")],
                                                   duration=delays[b.get_factor("Delay")])
                    if rt != None:
                        rt += display_time
                while exp.clock.time < time[i]:
                    new_button, _ = exp.keyboard.wait(keys=motricities[b.get_factor("Motricity")],
                                               duration=time[i]-exp.clock.time)
                    if new_button is not None:
                        multi_key_press.append((new_button, exp.clock.time - stim_onset))
                    pass
                i += 1
                answer = None if button == None else (is_right(button) == is_square_right)
                correct = None if answer == None else (answer == t.get_factor("Stimulus"))
                M += 1
                if rt != None :
                    S += rt
                    N += 1
                if correct != True: # False or None
                    E += 1
                if mode_id:
                    if len(multi_key_press) == 0:
                        exp.data.add([b.get_factor("BlockId"), serie_id, t.get_factor("TrialId"), 
                                      b.get_factor("Motricity"), b.get_factor("Eccentricity"), 
                                      b.get_factor("Delay"), t.get_factor("Stimulus"), 
                                      is_Rep, button, answer, correct, rt, stim_onset, 
                                      False, None, None,
                                      is_Pause])
                    else:
                        for info in multi_key_press:
                            exp.data.add([b.get_factor("BlockId"), serie_id, t.get_factor("TrialId"), 
                                      b.get_factor("Motricity"), b.get_factor("Eccentricity"), 
                                      b.get_factor("Delay"), t.get_factor("Stimulus"), 
                                      is_Rep, button, answer, correct, rt, stim_onset, 
                                      True, is_right(info[0]) == is_square_right, info[1],
                                      is_Pause])

            # inter-series pause
            if serie_id+1 < series_perblock[mode_id]:
                stimuli.TextScreen("Mini-pause", 
                                   "Appuyez sur " + key_string[pass_key] + 
                                   " pour continuer directement." + "\n" + 
                                   "Sinon, le bloc reprendra automatiquement dans quelques instants." 
                                   + ("\n\n" + "Temps de pause : "+str(t_minipause[mode_id]) + 
                                      " ms" if dev else "")).present()
                exp.keyboard.wait(keys=pass_key, duration=t_minipause[mode_id])

                inter.present()
                t0 = exp.clock.time
                while exp.clock.time < t0 + t_beginning :
                    pass

        # feedback
        if mode_id: 
            X += E/M
            if N>0:
                Y += S/N
                Z += 1
        stimuli.TextScreen("Feedback du bloc " + ("" if mode_id else "d'entraînement ") + "n°" 
                           + str(b.get_factor("BlockId")+1), 
                           "Taux de réussite : " 
                           + str(100-int((100*E)/M)) + "%" + "\n" + 
                           "Temps de réaction moyen : " 
                           + (str(int(S/N)) + " ms" if N>0 else "il faut répondre !")).present()
        exp.keyboard.wait(keys=pass_key, duration=t_feedback)

        # inter-block pause
        if mode_id:
            if b.get_factor("BlockId")+1 < 6:
                stimuli.TextScreen("Pause", 
                                   "Appuyez sur " + key_string[pass_key] + 
                                   " pour passer à la suite.").present()
                exp.keyboard.wait(keys=pass_key)
        else:
            if b.get_factor("BlockId") < 2:
                stimuli.TextScreen("Pause",
                                   "Veuillez attendre la consigne pour passer à la suite.").present()
                exp.keyboard.wait(keys=pass_key)
            elif b.get_factor("BlockId")+1 < 6:
                stimuli.TextScreen("Pause",
                                   "Appuyez sur " + key_string[pass_key] + 
                                   " pour passer à la suite.").present()
                exp.keyboard.wait(keys=pass_key)

    # end of mode screen
    if mode_id:
        stimuli.TextScreen("Expérience terminée", "Merci de votre participation !" + "\n\n" + 
                           "Appuyez sur " + key_string[pass_key] + 
                           " pour accéder à votre rémunération.").present()
        exp.keyboard.wait(keys=pass_key)
        csvwrite("gain.txt",f"{15+reward(100 * X/6):.1f} €")
        stimuli.TextScreen("Feedback de l'expérience", 
                           "Taux de réussite : " 
                           + (str(100 - int(100 * (X/6)))) + "%" + "\n" + 
                           "Temps de réaction moyen : " 
                           + str(int(Y/Z)) + " ms" + "\n\n" + 
                           "Vous touchez la rétribution suivante : " 
                           + f"{15+reward(100 * X/6):.1f} €" + 
                           ("\n\n" + "Statistiques" + "\n\n" + 
                            "X = " + str(X) + "\n" + 
                            "Y = " + str(Y) + "\n" + 
                            "Z = " + str(Z) if dev else "")).present()
        exp.keyboard.wait(keys=end_key)
    else:
        stimuli.TextScreen("Entraînement terminé", 
                           "Veuillez attendre la consigne pour passer à la suite.").present()
        exp.keyboard.wait(keys=pass_key)

control.end()