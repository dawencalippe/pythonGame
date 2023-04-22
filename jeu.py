# -*- coding: utf-8 -*-

import pygame
import random
import pygame.mixer
import time

# Initialisation de Pygame
pygame.init()

# Définir la vitesse de rafraîchissement de l'écran
FPS = 60

# Charger le son
son_collision = pygame.mixer.Sound("2361.wav")

# Utilisation de la police par défaut
police = pygame.font.SysFont(None, 30)

# Définition de la police d'écriture
font = pygame.font.SysFont('Arial', 30)

# Dimensions de la fenêtre
largeur = 1000
hauteur = 400
ecran = pygame.display.set_mode((largeur, hauteur))

# Création de la fenêtre
fenetre = pygame.display.set_mode((largeur, hauteur))

# Chargement de l'image de fond
fond = pygame.image.load("fond.jpg")
fond = pygame.transform.scale(fond, (largeur, hauteur)) # redimensionnement de l'image
pygame.display.set_caption("Jeu de tir")

# Création de l'horloge
horloge = pygame.time.Clock()

# Couleurs
blanc = (255, 255, 255)
noir = (0, 255, 0)
rouge = (255, 0, 0)
rouge = (255, 0, 0)
orange = (255, 128, 0)
jaune = (255, 255, 0)
vert_clair = (128, 255, 0)
vert_fonce = (0, 255, 0)
bleu_clair = (0, 255, 128)
bleu_fonce = (0, 128, 255)
violet = (128, 0, 255)
rose = (255, 0, 255)
blanc = (255, 255, 255)
doree = (255, 215, 0)

# Joueur
joueur_taille = 50
joueur_image = pygame.image.load("joueur.jpg").convert_alpha() 
# chargement de l'image du joueur
joueur_image = pygame.transform.scale(joueur_image, (joueur_taille, joueur_taille))

# redimensionnement de l'image
joueur_x = 10
joueur_y = (hauteur - joueur_taille) // 2
joueur_vitesse = 7

# Nouvel ennemi aléatoire
ennemi_taille = 50
ennemi_vitesse = 6
ennemi_x = largeur
ennemi_y = random.randint(0, hauteur - ennemi_taille)

# Score
score = 0

# Niveaux de difficulté
niveau = "DEV"


# Tir
tirs = []
tir_taille = 5
tir_x = joueur_x + joueur_taille
tir_y = joueur_y + joueur_taille // 2 - tir_taille // 2
tir_vitesse = 14
tir_actif = False
temps_ecoule = 0
couleur_tir = vert_fonce

# Décompte avant le début du jeu
compteur = 3

# Barre de score
barre_score_x = 20
barre_score_y = 20
barre_score_longueur = 300
barre_score_hauteur = 20

# Boucle principale du jeu
en_jeu = True
game_over = False 
last_shot_time = 0
shoot_delay = 0.1
while en_jeu:
    # Mesurer le temps écoulé depuis le début du programme
    current_time = time.time()
    
    # Calculer le temps écoulé depuis le dernier tir
    time_since_last_shot = current_time - last_shot_time
    
    # Gestion des événements
    for evenement in pygame.event.get():
        if evenement.type == pygame.QUIT:
            en_jeu = False
            game_over = True  # affichage de Game Over

    # Détection des touches enfoncées
    touches = pygame.key.get_pressed()
    if touches[pygame.K_UP]:
        joueur_y -= joueur_vitesse
    elif touches[pygame.K_DOWN]:
        joueur_y += joueur_vitesse
    elif touches[pygame.K_SPACE] and not tir_actif and time_since_last_shot >= shoot_delay:
        tir_x = joueur_x + joueur_taille
        tir_y = joueur_y + joueur_taille // 2 - tir_taille // 2      
        tirs.append([tir_x, tir_y, tir_taille, tir_vitesse, niveau])
        tir_actif = True
        last_shot_time = current_time
    
    
    # Vérification que le joueur est toujours à l'intérieur de la fenêtre
    if joueur_y < 0:
        joueur_y = 0
    elif joueur_y + joueur_taille > hauteur:
        joueur_y = hauteur - joueur_taille 

    
    # Déplacement de l'ennemi
    ennemi_x -= ennemi_vitesse

    # Vérification que l'ennemi est toujours à l'intérieur de la fenêtre
    if ennemi_x + ennemi_taille < 0:
        ennemi_x = largeur
        ennemi_y = random.randint(0, hauteur - ennemi_taille)
        

    # Gestion des collisions avec le joueur
    if ennemi_x < joueur_x + joueur_taille and ennemi_x + ennemi_taille > joueur_x and ennemi_y < joueur_y + joueur_taille and ennemi_y + ennemi_taille > joueur_y:
        # Collision détectée, arrêter le jeu ou réinitialiser le joueur
        en_jeu = False
        game_over = True

    # Détection de collision entre le tir et l'ennemi
    if tir_actif:
        for tir in tirs:
            if ennemi_y + ennemi_taille > tir[1] and ennemi_y < tir[1] + tir[2] and ennemi_x + ennemi_taille > tir[0] and ennemi_x < tir[0] + tir[2]:
                ennemi_x = random.randint(0, largeur - ennemi_taille)
                ennemi_y = -ennemi_taille
                son_collision.play()
                tirs.remove(tir)
                tir_actif = False
                score += 1  # Augmentation du score de 1

    # Gestion des tirs
    temps_ecoule = horloge.tick(FPS)
    temps_ecoule_secondes = temps_ecoule / 1000.0 
    if temps_ecoule > 1000:  # permet de tirer toutes les 500 millisecondes
        if touches[pygame.K_SPACE]:
            tir_x = joueur_x + joueur_taille
            tir_y = joueur_y + joueur_taille // 2 - tir_taille // 2      
            tirs.append([tir_x, tir_y, tir_taille, tir_vitesse, niveau])
            tir_actif = True
            temps_ecoule = 0  # réinitialise le temps écoulé

    # Déplacement du tir
    for tir in tirs:
        tir[0] += tir[3] * temps_ecoule_secondes
        if tir[0] > largeur:
            tirs.remove(tir)
            tir_actif = False
    
    # Suppression des tirs qui ont atteint la fin de l'écran
    tirs = [tir for tir in tirs if tir[0] < largeur]
    # Effacer les anciennes positions du tir et de l'ennemi
    ecran.blit(fond, (0, 0))
    

    
    # Afficher le texte "Game Over" pendant 5 secondes avant de fermer la fenêtre
    if game_over:
        temps_ecoule = pygame.time.get_ticks()
        if temps_ecoule < 8000:  # attendre 5 secondes
            police_game_over = pygame.font.SysFont("monospace", 80)
            texte_game = police_game_over.render("Game", True, (255, 0, 0))
            texte_over = police_game_over.render("Over", True, (255, 255, 255))
            ecran.blit(texte_game, (largeur // 2 - texte_game.get_width() // 2, hauteur // 2 - texte_game.get_height()))
            ecran.blit(texte_over, (largeur // 2 + texte_game.get_width() // 2, hauteur // 2 - texte_over.get_height()))
        else:
            en_jeu = False  # fermer la fenêtre
    # Affichage
    ecran.blit(joueur_image, (joueur_x, joueur_y))
    ecran.blit(joueur_image, (ennemi_x, ennemi_y))
    # Dessin de la barre de score
    if score <= 5:
       couleur_barre = rouge
    elif score <= 10:
       couleur_barre = orange
    elif score <= 20:
       couleur_barre = jaune
    elif score <= 40:
       couleur_barre = vert_clair
    elif score <= 50:
       couleur_barre = vert_fonce
    elif score <= 60:
       couleur_barre = bleu_clair
    elif score <= 70:
       couleur_barre = bleu_fonce
    elif score <= 80:
       couleur_barre = violet
    elif score <= 90:
       couleur_barre = rose
    else:
       couleur_barre = blanc
       
    barre_score_longueur_remplie = int(barre_score_longueur * score / 100) # ratio de la longueur remplie par rapport au score
    pygame.draw.rect(ecran, couleur_barre, (barre_score_x, barre_score_y, barre_score_longueur_remplie, barre_score_hauteur))
    pygame.draw.rect(ecran, noir, (barre_score_x, barre_score_y, barre_score_longueur, barre_score_hauteur), 2)
    
    # Affichage du tir
    if tir_actif:
        # Affichage des tirs
        for tir in tirs:
            if tir[4] == "DEV":
                couleur_tir = rouge
            elif tir[4] == "PO":
                couleur_tir = bleu_clair
            elif tir[4] == "EM":
                couleur_tir = doree
            pygame.draw.rect(ecran, couleur_tir, (tir[0], tir[1], tir[2], tir[2]))
            tir[0] += tir[3]
            if tir[0] > largeur:
                tirs.remove(tir)
                tir_actif = False
                
    # Vérification du score pour changer de niveau
    if score >= 5:
        niveau = "PO"
    if score >= 10:
        niveau = "EM"
        
    niveau_texte = font.render(niveau, True, (255, 255, 255))
    niveau_rect = niveau_texte.get_rect()
    niveau_rect.centerx = largeur // 2
    niveau_rect.top = 10
    fenetre.blit(niveau_texte, niveau_rect)

    
    # Affichage du score et du temps de jeu
    score_texte = font.render(str(score), True, rouge)

    # Création de la surface du cercle doré
    rayon = 20
    surface_cercle = pygame.Surface((2*rayon, 2*rayon), pygame.SRCALPHA)
    pygame.draw.circle(surface_cercle, doree, (rayon, rayon), rayon)
    
    # Affichage du cercle doré et du score
    ecran.blit(surface_cercle, (largeur-40, 10))
    ecran.blit(score_texte, (largeur-40+rayon-score_texte.get_width()//2, 10+rayon-score_texte.get_height()//2)) 
 
    # Rafraîchir l'écran
    pygame.display.update()

    
# Attendre 8 secondes avant de fermer la fenêtre
pygame.time.delay(5000)


# Fermeture de Pygame
pygame.quit()