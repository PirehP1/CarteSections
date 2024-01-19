"""
Created on Janv 18 23:29:20 2024
@author: Stephane Lamassé
Institutions: Pireh-Lamop
LICENCE GNU
Le but de ce script est d'afficher deux graphiques : une grille de carrés colorés en fonction des sections et intensités,
et une grille de texte en dessous de la première grille.
"""

#import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.gridspec as gridspec
import random



# Définition de la fonction pour créer les carrés colorés
def create_squares(sections, color_intensities, grid_width, square_size, space, colormap):
    """
    Crée des carrés colorés en fonction des sections et intensités fournies.

    Paramètres :
    - sections : Liste des sections.
    - color_intensities : Liste des intensités de couleur.
    - grid_width : Largeur de la grille.
    - square_size : Taille des carrés.
    - space : Espacement entre les carrés.
    - colormap : Carte de couleurs.

    Retourne :
    - Liste d'objets de type `Rectangle` de Matplotlib représentant les carrés.
    """
    squares = []

    # réajustement pour changer l'origine du graphique (0,0) en haut à gauche
    nb_element = len(sections)
    tab_width = []
    # création des positions width par rapport à la taille de la grille
    for i in range(grid_width):
        tab_width.append(i * (space + square_size))
    n_height = 0

    # ajout des indices de la taille dans un tableau
    while nb_element > 0:
        n_height += 1
        nb_element -= grid_width

    tab_final = []

    # ajout dans un tableau de tuple des positions finales et calcul de la taille par rapport à l'indice
    while n_height > 0:
        for j in range(len(tab_width)):
            if len(sections) % grid_width  == 0:
                tab_final.append((tab_width[j], (n_height * (space + square_size))))
            else:
                tab_final.append((tab_width[j], (n_height * (space + square_size)) - square_size ))

        n_height -= 1

    for i, (section, intensity) in enumerate(zip(sections, color_intensities)):

        # Récupéraion de la position
        element = tab_final[i]
        #print(element)
        x_position = element[0]
        y_position = element[1]   # Calcul de la couleur en fonction de l'intensité

        intensity_color = colormap(intensity)

        # Création d'un carré et ajout à la liste
        square = patches.Rectangle((x_position, y_position), square_size, square_size,
                                   linewidth=1, edgecolor='black', facecolor=intensity_color)
        squares.append(square)

    return squares

# Définition de la fonction pour mettre à jour le texte en dessous de la grille

def ajuster_coordonnees(hauteur, x, y):
    """
    Retranscris l'origine des coordonnées en haut à gauche de la grille

    Paramètres :
    - hauteur : la hauteur de la grille --> calculé avec la fonction add_index
    - x : Coordonnée de la ligne
    - y : Coordonnée de la colonne
    """
    coord_x = x
    coord_y = hauteur - y - 1
    return (coord_x, coord_y)

def add_index(col, row, sections, grid_width):
        """
        Renvoi l'index de l'élément qui correspond au rectangle par rapport à la grille

        Note : Le clic n'est pas très précis

        Paramètres :
        - col : position clic x
        - row : position clic y
        - sections : sections --> pour trouver le nombre de rectangle
        - grid_width : Taille de la grille
        """

        # recupération de l'index
        # Quand la taille de la grille est un multiple de la taille de sections
        if len(sections) % grid_width  == 0:
            n_height = 0
            nb_element = len(sections)
            # ajout des indices de la taille dans un tableau
            while nb_element > 0:
                n_height += 1
                nb_element -= grid_width
            n_height +=1
            ind = ajuster_coordonnees(n_height, col, row)
            ind_x = ind[0]
            ind_y = ind[1]

        # Quand la taille de la grille n'est pas un multiple de la taille de sections
        else:
            n_height = 0
            nb_element = len(sections)
            # ajout des indices de la taille dans un tableau
            while nb_element > 0:
                # augmentation de la taille pour palier à la colonne manquante
                n_height += 1
                nb_element -= grid_width
            ind = ajuster_coordonnees(n_height, col, row)
            ind_x = ind[0]
            ind_y = ind[1]
            print(ind_x, ind_y)

        index = ind_y * grid_width + ind_x
        return index

def update_text(event, sections, texte, text_box, grid_width, square_size, space_before_text):
    """
    Met à jour le texte en dessous de la grille en fonction de la position du curseur de la souris.

    Paramètres :
    - event : Événement de clic de souris.
    - sections : Liste des sections.
    - texte : Liste du texte associé à chaque section.
    - text_box : Objet Text de Matplotlib utilisé pour afficher le texte.
    - grid_width : Largeur de la grille.
    - square_size : Taille des carrés.
    - space_before_text : Espacement avant le texte.
    """
    if event.xdata is not None and event.ydata is not None:
        col = int(event.xdata)
        row = int(event.ydata)

        # récupération de l'index
        index = add_index(col, row, sections, grid_width)

        if 0 <= index < len(sections):
            text_content = texte[index]

            # Mise à jour de la position du texte en dessous de la grille
            text_box.set_position((0, -space_before_text))  # Ajustement de l'espace

            # Mise à jour du texte
            text_box.set_text(text_content)
            plt.draw()

# Définition de la fonction principale pour afficher les deux grilles
def plot_squares(sections, intensities, texte, grid_width=4, cmap='viridis', title_of_grid= "Carte des sections"):
    """
    Crée et affiche deux grilles : une grille de carrés colorés et une grille de texte en dessous.

    Paramètres :
    - sections : Liste des sections.
    - intensities : Liste des intensités de couleur.
    - texte : Liste du texte associé à chaque section.
    - grid_width : Largeur de la grille (par défaut à 4).
    - cmap : Carte de couleurs (par défaut à 'viridis').
    """
    num_squares = len(sections)

    # Définition de la grille principale avec gridspec
    gs = gridspec.GridSpec(2, 1, height_ratios=[num_squares // grid_width + 1, 1])

    # Sous-grille pour les carrés colorés
    ax0 = plt.subplot(gs[0])
    square_size = 0.8
    space = 0.025
    colormap = plt.get_cmap(cmap)
    squares = create_squares(sections, intensities, grid_width, square_size, space, colormap)
    for square in squares:
        ax0.add_patch(square)

    ax0.set_xlim(0, grid_width * (square_size + space) - space)
    ax0.set_ylim(0, (num_squares // grid_width + 1) * (square_size + space) - space)
    ax0.set_xticks([])
    ax0.set_yticks([])

    # Sous-grille pour le texte
    ax1 = plt.subplot(gs[1])
    ax1.set_xlim(ax0.get_xlim())
    ax1.set_ylim(-1, 1)  # Ajustez selon vos besoins
    ax1.axis('off')

    space_before_text = 0.1
    text_box = ax1.text(0, -space_before_text, "Cliquez sur la section pour afficher le texte en dessous", ha='left', va='center', fontsize=10,
                        bbox=dict(facecolor='white', alpha=0.7, edgecolor='black'))

    # Fonction de mise à jour du texte lors d'un clic de souris
    def update_text_on_click(event):
        update_text(event, sections, texte, text_box, grid_width, square_size, space_before_text)

    # Connexion de la fonction de mise à jour au clic de souris
    fig = plt.gcf()
    fig.canvas.mpl_connect('button_press_event', update_text_on_click)


    # Ajout du titre global à la grille
    plt.suptitle(title_of_grid, fontsize=14)

    # Affichage des graphiques
    plt.show()



# Exemple d'utilisation avec les nouvelles données
sections = [1, 1, 1, 1, 2, 2,3,3,4]
intensities = [0.5, 0.3, 0.5, 0.7, 0.0, 0.4, 0.2,0.2,0.90]
texte = ["Ce script", "a été produit", "par Stéphane Lamassé", "sur l'inspiration des cartes de sections de Lexico3", ". Et cela, dans le cadre d'une recherche conduite", "à l'Université Paris 1 Panthéon-Sorbonne", " dans l'équipe du Pireh", "", ""]

grid_width = 3

# Appel de la fonction principale pour afficher les graphiques
plot_squares(sections, intensities, texte, grid_width=grid_width, cmap='inferno')
