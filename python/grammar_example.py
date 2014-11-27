from grammar import Grammar
import pygame.midi
import time

def chord(player, sound):
    player.set_instrument(33,1)
    player.note_on(sound-12, 125,1)
    player.set_instrument(25,1)
    player.note_on(sound, 125,1)
    player.note_on(sound + 4, 125,1)
    player.note_on(sound + 7, 125,1)
    player.note_on(sound + 12, 125,1)
    time.sleep(0.2)
    player.note_off(sound, 125,1)
    player.note_off(sound + 4, 125,1)
    player.note_off(sound + 7, 125,1)
    player.note_off(sound + 12, 125,1)
    player.note_off(sound-12, 125,1)

def main():
    pygame.midi.init()
    player= pygame.midi.Output(0)
    player.set_instrument(25,1)

    sounds = {'C': 48, 'F': 53,'G': 55}

    nonterminals = ['q', 'w']

    productions = {'q': [("CCCq", 1), ("FGw", 1)], 'w': [("FCCq", 1)]}

    gr = Grammar("q", nonterminals, productions)

    while True:
        gr.make_production()
        music = gr.show_word()
        for note in music:
            chord(player, sounds[note])
            
            
if __name__ == "__main__":
    main()