import pygame
import sys
import CHIP8 as chp8
from tkinter import Tk, filedialog

###############################  PYGAME  ###############################

# Initialisation de pygame
pygame.init()
# Initialisation de la fenêtre
largeur = 640
hauteur = 320

# Création de la fenêtre
ecran = pygame.display.set_mode((largeur, hauteur), pygame.RESIZABLE)

# Nom de la fenêtre
pygame.display.set_caption("Emulateur CHIP-8")

# Icon et fond de la fenetre 
pygame.display.set_icon(pygame.image.load("ressource/image/icon.png"))
fond = pygame.image.load("ressource/image/fond.png")
fond = pygame.transform.scale(fond, (largeur, hauteur))


# Couleurs
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
ROUGE = (255, 0, 0)
GRIS = (200, 200, 200)

# Charger la police personnalisée
font = pygame.font.Font("ressource/font/retro.ttf", 19)

###############################  TKINTER  ###############################

# Fonction pour ouvrir une boîte de dialogue de sélection de fichier
def ouvrir_boite_dialogue():
    root = Tk()
    root.withdraw()  # Cacher la fenêtre principale de Tkinter
    fichier = filedialog.askopenfilename(title="Sélectionnez votre jeux CHIP-8", filetypes=[("Fichiers ROM", "*.ch8 *.rom")])
    return fichier

###############################  BOUTON  ###############################

# Dimension des 2 boutons
bouton_largeur = 225
bouton_hauteur = 50

# Marge bouton Fichier 
marge_bas_fichier = 20

# Position du bouton Fichier
bouton_fichier_x = (largeur // 2) - (bouton_largeur // 2)
bouton__fichier_y = hauteur - bouton_hauteur - marge_bas_fichier

# Définir le bouton Fichier 
bouton_fichier_rect = pygame.Rect(bouton_fichier_x, bouton__fichier_y, bouton_largeur, bouton_hauteur)
bouton_fichier_texte = "Choisir un fichier"
bouton_couleur = GRIS

# Marge bouton Options 
marge_bas_options  = 90

# Position du bouton Options
bouton_options_x = (largeur // 2) - (bouton_largeur // 2)
bouton_options_y = hauteur - bouton_hauteur - marge_bas_options

# Définir le bouton Options
bouton_options_rect = pygame.Rect(bouton_options_x, bouton_options_y, bouton_largeur, bouton_hauteur)
bouton_options_texte = "Lancer"
bouton_couleur = GRIS

#Definir le Fichier
Fichier = ""
###############################  BOUCLE, EVENEMENTS  ###############################

# Boucle principale
en_cour = True
while en_cour:
    if fond:
        ecran.blit(fond, (0, 0))
    else:
        ecran.fill(NOIR)

    # Dessiner le bouton Fichier
    pygame.draw.rect(ecran, bouton_couleur, bouton_fichier_rect)
    texte_surface = font.render(bouton_fichier_texte, True, NOIR)
    texte_rect = texte_surface.get_rect(center=bouton_fichier_rect.center)
    ecran.blit(texte_surface, texte_rect)

    # Dessiner le bouton Options
    pygame.draw.rect(ecran, bouton_couleur, bouton_options_rect)
    texte_surface = font.render(bouton_options_texte, True, NOIR)
    texte_rect = texte_surface.get_rect(center=bouton_options_rect.center)
    ecran.blit(texte_surface, texte_rect)
    # Gestion des événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            en_cour = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                en_cour = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            souris_pos = pygame.mouse.get_pos()
            if bouton_fichier_rect.collidepoint(souris_pos):  # Vérifier si le clic est sur le bouton
                fichier = ouvrir_boite_dialogue()
                if fichier:
                    Fichier = fichier
                    print(Fichier)
            if bouton_options_rect.collidepoint(souris_pos) and Fichier!="*.ch8":  # Vérifier si le clic est sur le deuxième bouton
                    chip = chp8.CHIP8(Fichier)
                    chip.Mainchip8()
    # Mettre à jour la fenêtre
    pygame.display.flip()

# Fermeture de pygame
pygame.quit()
sys.exit()