import pygame
import sys
import math
import random
import time


pygame.init()
largeur, hauteur = 800, 600
fenetre = pygame.display.set_mode((largeur, hauteur))
pygame.display.set_caption("Titre")
niv_actu = 0
son = pygame.mixer.Sound("ressources/music1.mp3")
saut_son = pygame.mixer.Sound("ressources/launch.wav")
charge_son = pygame.mixer.Sound("ressources/charge.wav")
spawn_son = pygame.mixer.Sound("ressources/spawn.wav")
mort_son = pygame.mixer.Sound("ressources/spontaneous_death.wav")
bg_images = []
for i in range(1, 6):
    bg_image = pygame.image.load(f"ressources/bg/{niv_actu}/{i}.png").convert_alpha()
    bg_images.append(bg_image)
bg_width = bg_images[0].get_width()


taille_bloc = 55
vie = 3
son.play()
particule_active = False



def draw_bg():
    for i, bg_image in enumerate(bg_images):
        speed = (i + 1) * 0.2
        x_offset = (scroll * speed) % bg_width
        fenetre.blit(bg_image, (x_offset - bg_width, 0))
        fenetre.blit(bg_image, (x_offset, 0))

def affiche_niveau(niv_actu):

    texte = f"Niveau {niv_actu}"
    font = pygame.font.Font("ressources/altertype-Regular.otf", 100)
    texte_image = font.render(texte, True, (255, 255, 255)) 

    rect = texte_image.get_rect()
    rect.center = fenetre.get_rect().center

    for alpha in range(255, -1, -5): 
        image = texte_image.copy()
        image.fill((255, 255, 255, alpha), None, pygame.BLEND_RGBA_MULT)

        fenetre.blit(image, rect)

        pygame.display.flip()

        time.sleep(0.01)  
class Camera:
    def __init__(self, largeur, hauteur):
        self.x = 0
        self.y = 0
        self.largeur = largeur
        self.hauteur = hauteur
        self.rect = pygame.Rect(self.x, self.y, self.largeur, self.hauteur)

    def update(self, target):
        self.x = target.x - self.largeur // 2 + target.taille // 2
        self.y = target.y - self.hauteur // 2 + target.taille // 2
        self.rect = pygame.Rect(self.x, self.y, self.largeur, self.hauteur)
class Particulee:
    def __init__(self, x, y, vx, vy, vie):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.vie = vie
"""def enregistrer_meilleur_score(score, niv_actu):
    nom_fichier = f"meilleur_score_niv{niv_actu}.txt"
    try:
        # On essaye d'ouvrir le fichier en mode lecture
        with open(f'meilleur_score_niv0.txt', "r") as fichier:
            # Si le fichier existe, on récupère le meilleur score
            meilleur_score = float(fichier.read())
    except FileNotFoundError:
        # Si le fichier n'existe pas, on considère que le meilleur score est 0
        meilleur_score = 0

    # On compare le score actuel au meilleur score
    if score < meilleur_score:
        # Si le score actuel est meilleur, on le sauvegarde
        with open(f'meilleur_score_niv0.txt', "w") as fichier:
            fichier.write(str(score))
        return score
    else:
        # Sinon, on retourne le meilleur score précédent
        return meilleur_score

def lire_meilleur_score(niveau):
    try:
        with open(f'meilleur_score_niv0.txt', 'r') as fichier:
            meilleur_score = fichier.read()
            if meilleur_score:  # vérifie que la chaîne n'est pas vide
                return float(meilleur_score)
    except FileNotFoundError:  # si le fichier n'existe pas
        pass

    # Si le fichier est vide ou n'existe pas, renvoyer 0
    return 0"""

def write_to_file(niv_actu, text):
    with open(f"mon_fichier.txt", 'w') as file:
        file.write(str(text))

def read_from_file(niv_actu, score):
    with open(f"mon_fichier.txt", 'r') as file:
        content = file.read()
        float(content)
    if score < float(content) or float(content) ==0:
        with open(f"mon_fichier.txt", 'w') as file:
            file.write(str(score))
def read(niv_actu):
    with open(f"mon_fichier.txt", 'r') as file:
        content = file.read() 
        return content
    
# Usage
#write_to_file('mon_fichier.txt', 'Bonjour, monde !')


class Personnage:
    
    def __init__(self, x, y, taille):
        self.x = x
        self.y = y
        self.taille = taille
        self.vx = 0
        self.vy = 0
        self.sur_le_sol = False
        self.vie = vie
        self.graviter = True 
 
    def deplacer(self, dx, dy):
        self.x += dx
        self.y += dy
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.taille, self.taille)
    
    def dessiner(self, fenetre, camera):
        dessiner_cotes_bloc_3d(fenetre, (215,137,11), self.x - camera.x, self.y-camera.y,self.taille, 10, 1)
        dessiner_face_superieure_bloc_3d(fenetre, (236,123,29), self.x - camera.x, self.y-camera.y,self.taille, 10, 1)
    def maj_vitesse(self, gravite):
            self.vy += gravite
            
    def collision(self, taille_bloc):
        global niv_actu
        self.sur_le_sol = False
        perso_rect = pygame.Rect(self.x , self.y, (self.taille)-1, (self.taille)-1)
        self.collision_verif = False

        perso_rect.x += self.vx
        perso_rect.y += self.vy
        new_x = self.x
        new_y = self.y
        
        for i, ligne in enumerate(niveau[niv_actu]):
            for j, bloc in enumerate(ligne):
                if bloc == 1 :
                    bloc_rect = pygame.Rect(j * taille_bloc, i * taille_bloc, taille_bloc, taille_bloc)
                    if perso_rect.colliderect(bloc_rect):
                        dx = min(abs(perso_rect.right - bloc_rect.left), abs(perso_rect.left - bloc_rect.right))
                        dy = min(abs(perso_rect.top - bloc_rect.bottom), abs(perso_rect.bottom - bloc_rect.top))

                        if dx < dy:
                            if perso_rect.right > bloc_rect.left and self.vx > 0:
                                self.vx = 0
                                new_x = bloc_rect.left - self.taille 
                            if perso_rect.left < bloc_rect.right and self.vx < 0:
                                self.vx *= -0.2
                                new_x = bloc_rect.right
                        else:
                            if perso_rect.top < bloc_rect.bottom and self.vy < 0:
                                self.vy = 0
                                new_y = bloc_rect.bottom 
                            if perso_rect.bottom > bloc_rect.top and self.vy > 0:
                                self.vy = 0
                                new_y = bloc_rect.top - self.taille
                                self.sur_le_sol = True   
                if bloc == 2:
                    bloc_rect = pygame.Rect(j * taille_bloc, i * taille_bloc, taille_bloc, taille_bloc)
                    if perso_rect.colliderect(bloc_rect):
                        personnage.taille = 1
                    else : 
                        personnage.taille = 25
                
                if bloc == 3 :
                    bloc_rect = pygame.Rect(j * taille_bloc, i * taille_bloc, taille_bloc, taille_bloc)
                    if perso_rect.colliderect(bloc_rect):
                        dx = min(abs(perso_rect.right - bloc_rect.left), abs(perso_rect.left - bloc_rect.right))
                        dy = min(abs(perso_rect.top - bloc_rect.bottom), abs(perso_rect.bottom - bloc_rect.top))

              
                        if perso_rect.bottom > bloc_rect.top and self.vx > 0:
                            self.vy -= 18
                            self.vx += 1.3
                            new_y = bloc_rect.top - self.taille   
                        if perso_rect.bottom > bloc_rect.top and self.vx < 0:
                            self.vy -= 18
                            self.vx *=1.3
                            new_y = bloc_rect.top - self.taille
                             
                if bloc == 4:
                    bloc_rect = pygame.Rect(j * taille_bloc, i * taille_bloc, taille_bloc, taille_bloc)
                    if perso_rect.colliderect(bloc_rect):
                        dx = min(abs(perso_rect.right - bloc_rect.left), abs(perso_rect.left - bloc_rect.right))
                        dy = min(abs(perso_rect.top - bloc_rect.bottom), abs(perso_rect.bottom - bloc_rect.top))

                        if dx < dy:
                            if perso_rect.right > bloc_rect.left and self.vx > 0:
                                self.vx -= 20
                                new_x = bloc_rect.left - self.taille 
                            if perso_rect.left < bloc_rect.right and self.vx < 0:
                                self.vx += 20
                                new_x = bloc_rect.right
                        else:
                            if perso_rect.top < bloc_rect.bottom and self.vy < 0:
                                self.vy = 0
                                new_y = bloc_rect.bottom 
                            if perso_rect.bottom > bloc_rect.top and self.vy > 0:
                                self.vy = 0
                                new_y = bloc_rect.top - self.taille
                                self.sur_le_sol = True                   
                if bloc == 5:
                    bloc_rect = pygame.Rect(j * taille_bloc, i * taille_bloc, taille_bloc, taille_bloc)
                    if perso_rect.colliderect(bloc_rect):
                        new_x, new_y = 300,300
                        self.vx, self.vy = 0,0
                        self.vie -= 1
                        son_mort = True
                

                if bloc == 6:
                    bloc_rect = pygame.Rect(j * taille_bloc, i * taille_bloc, taille_bloc, taille_bloc)
                    if perso_rect.colliderect(bloc_rect):
                        temps_fin = time.time()  # arrêter le chronomètre
                        score = temps_fin - temps_debut  # calculer le score
                        write_to_file("mon_fichier.txt", score)
                        read_from_file("mon_fichier.txt", score)
                        niv_actu += 1
                        self.x, self.y = 300,300
                        self.vx, self.vy = 0,0
                        affiche_niveau(niv_actu)

                if bloc == 9 :
                    if (pygame.time.get_ticks() // 2000) % 2 == 0:
                        bloc_rect = pygame.Rect(j * taille_bloc, i * taille_bloc, taille_bloc, taille_bloc)
                        if perso_rect.colliderect(bloc_rect):
                            dx = min(abs(perso_rect.right - bloc_rect.left), abs(perso_rect.left - bloc_rect.right))
                            dy = min(abs(perso_rect.top - bloc_rect.bottom), abs(perso_rect.bottom - bloc_rect.top))

                            if dx < dy:
                                if perso_rect.right > bloc_rect.left and self.vx > 0:
                                    self.vx = 0
                                    new_x = bloc_rect.left - self.taille 
                                if perso_rect.left < bloc_rect.right and self.vx < 0:
                                    self.vx = 0
                                    new_x = bloc_rect.right
                            else:
                                if perso_rect.top < bloc_rect.bottom and self.vy < 0:
                                    self.vy = 0
                                    new_y = bloc_rect.bottom 
                                if perso_rect.bottom > bloc_rect.top and self.vy > 0:
                                    self.vy = 0
                                    new_y = bloc_rect.top - self.taille
                                    self.sur_le_sol = True          
        self.x = new_x
        self.y = new_y




    
    
class Particule:
    def __init__(self, x, y, taille, couleur, duree_vie):
        self.x = x
        self.y = y
        self.taille = taille
        self.couleur = couleur
        self.duree_vie = duree_vie

    def update(self):
        self.duree_vie -= 1

    def draw(self, surface, camera):
        if self.duree_vie > 0:
            pygame.draw.rect(surface, self.couleur, (int(self.x)- camera.x, int(self.y)- camera.y, self.taille, self.taille))

class TrailParticle:
    def __init__(self, x, y, size, color=(0, 0, 0), lifetime=10):
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.lifetime = lifetime

    def update(self):
        self.lifetime -= 1

    def draw(self, surface):
        if self.lifetime > 0:
            alpha = int(255 * (self.lifetime / 50))
            transparent_color = (*self.color, alpha)
            pygame.draw.circle(surface, transparent_color, (self.x + self.size // 2, self.y + self.size // 2), self.size // 2)

class WaterParticle:
    def __init__(self, x, y, size, speed, camera):
        self.x = x
        self.y = y
        self.size = size
        self.speed = speed
        self.camera = camera
        self.rect = pygame.Rect(x - camera.x, y - camera.y, size, size)

"""class Score:
    def Best_score(perso_rect) :
        if event.type == pygame.MOUSEBUTTONUP:
            if deplacement_actif:
                debut_course=time.time()
                for i, ligne in enumerate(niveau[niv_actu]):
                    for j, bloc in enumerate(ligne):
                        if bloc == 6:
                            bloc_rect = pygame.Rect(j * taille_bloc, i * taille_bloc, taille_bloc, taille_bloc)
                            if perso_rect.colliderect(bloc_rect):
                                fin_course = time.time()
                score = fin_course - debut_course
                #return score
                print(score)"""
                
def generate_water_particles(niveau, taille_bloc, camera, generation_probability=0.02):
    water_particles = []
    for i, ligne in enumerate(niveau):
        for j, bloc in enumerate(ligne):
            if bloc == 5:
                if random.random() < generation_probability:
                    x = j * taille_bloc + random.randint(0, taille_bloc)
                    y = i * taille_bloc + random.randint(0, taille_bloc)
                    size = random.randint(2, 5)
                    speed = random.uniform(0.5, 1.5)
                    water_particle = WaterParticle(x, y, size, speed, camera)
                    water_particles.append(water_particle)
    return water_particles




def create_explosion(x, y, particule):
    for _ in range(30): 
        particles.append(Particule(x, y))


def creer_particules(x, y, tailles, couleurs, duree_vie, nombre_particules):
    particules = []
    for _ in range(nombre_particules):
        taille = random.choice(tailles)
        couleur = random.choice(couleurs)
        dx = random.randint(-taille, taille)
        dy = random.randint(-taille, taille)
        particule = Particule(x + dx, y + dy, taille, couleur, duree_vie)
        particules.append(particule)
    return particules


niveau = [[[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], #INTRODUCTION
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0],
[0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,6,6,0,0,0,0,0,0],
[0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,7,0,0,7,0,0,7,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,6,6,0,0,0,0,0,0],
[0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,6,6,0,0,0,0,0,0],
[0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0],
[0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,8,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,9,9,4,4,0,0,0,0,0,0,0,0,0,1,1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1,2,2,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[1,1,1,1,1,1,1,1,1,0,0,0,0,1,1,1,0,0,1,1,0,0,1,1,1,1,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,1,1,1,1,1,1,1,0,0,0,0,1,1,1,0,0,1,1,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,1,0,0,1,5,5,5,5,5,5,5,5,5,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,1,1,1,1,1,1,1,5,5,5,5,1,1,1,5,5,1,1,5,5,1,1,1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,1,0,0,1,5,5,5,5,5,5,5,5,5,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,1,1,1,1,1,1,1,5,5,5,5,1,1,1,5,5,1,1,5,5,1,1,1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,1,0,0,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,1,1,1,1,1,1,1,5,5,5,5,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,1,1,1,3,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,1,1,1,1,1,1,1,5,5,5,5,1,1,1,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]],
          
    [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], #NIVEAU 1
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,1,0,0,1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,5,5,5,5,1,0,0,1,0,0,0,0,1,0,0,0,0,0,0,0,1,1,1,0,7,7,0,7,7,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,1,0,0,1,1,0,1,0,0,0,0,0,0,1,1,1,1,1,1,0,0,1,1,1,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,1,0,0,1,1,0,1,0,0,0,0,0,0,0,0,7,7,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,1,0,0,7,7,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,7,0,1,0,0,0,0,0,1,0,0,0,0,1,1,1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,1,0,0,0,0,0,7,0,0,0,0,0,1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,1,1,1,1,1,0,1,0,0,0,0,1,0,1,1,0,0,0,1,0,0,0,0,0,1,1,1,1,1,1,0,0,0,0,0,0],
[0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,1,1,0,0,1,1,0,0,1,0,0,0,0,1,1,0,0,0,0,1,1,0,0,0,0,0],
[0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,1,0,0,1,5,5,1,1,5,5,1,1,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,1,0,0,0,0,1,0,0,1,0,0,0,1,1,0,0,0,0,0,0,1,1,1,0,0,0],
[0,0,0,1,0,0,0,0,0,0,0,0,0,0,1,1,0,0,1,1,1,1,1,1,1,1,1,0,0,0,1,1,1,0,0,0,0,0,1,1,1,0,0,0,1,0,0,0,0,1,0,0,1,1,0,0,1,0,0,0,0,0,0,0,0,0,1,1,0,0],
[1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,8,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,1,0,0,7,1,1,1,1,0,0,0,8,8,0,0,0,0,7,1,1,1],
[1,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,1,1,1,0,0,0,0,0,6,6],
[1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,0,0,0,0,3,1,1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,1,1,1,0,0,0,0,0,6,6],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,8,8,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,1,1,1,1,0,0,0,0,0,7,0,0,0,8,1,1,1],
[1,1,1,1,0,0,1,1,0,0,0,0,0,0,0,0,0,0,1,1,0,0,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,1,0,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0,1,1,0,0],
[0,0,1,1,0,0,1,1,0,0,0,8,8,0,0,0,0,0,0,0,0,0,0,0,0,8,0,1,0,0,0,1,1,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,1,1,0,0,0,0,0,0,1,1,1,0,0,0],
[0,0,1,1,5,5,1,1,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,1,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,1,0,0,1,1,5,5,5,5,1,1,0,0,0,0,0],
[0,0,1,1,5,5,1,1,5,5,5,1,1,1,1,0,0,0,0,1,0,0,0,0,8,0,8,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,1,0,0,0,1,1,1,1,1,1,0,0,0,0,0,0],
[0,0,1,1,5,5,1,1,5,5,5,1,1,5,5,5,5,5,5,1,5,5,1,1,1,1,1,1,5,5,5,5,5,5,5,5,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,3,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,1,1,5,5,1,1,5,5,5,1,1,5,5,5,5,5,5,1,5,5,1,1,1,1,1,1,5,5,5,5,5,5,5,5,1,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]],

[ [ 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], #NIVEAU 2
[ 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[ 0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,1,0,7,0,0,0,0,0,7,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[ 0,0,1,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[ 0,0,1,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[ 0,0,1,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,1,0,1,0,0,0,1,0,0,0,1,1,1,0,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[ 0,0,1,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,1,0,1,0,0,0,7,0,0,0,0,7,0,0,0,0,7,0,0,1,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
[ 0,0,1,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0],
[ 0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,7,0,1,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0],
[ 0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,0,0,0,0,0,0,7,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1,1,1,0,0,0,0,0,1,0],
[ 0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1,0,0,0,0,0,0,0,0,7,0,1,0,0,0,0,0,0,1,1,9,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,0,1,0],
[ 0,0,1,1,1,1,0,0,0,0,0,0,0,0,1,1,1,1,0,0,1,0,0,0,0,0,0,0,0,0,0,7,0,0,0,0,0,0,0,0,9,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,1,1,0,0,0,0,1,0],
[ 0,0,0,0,0,1,5,5,5,5,5,5,5,5,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,2,0,0,0,0,0,0,1,1,1,0,0,0,0,1,0,1,0,0,0,1,7,0,0,0,0,1,0],
[ 0,0,0,0,0,1,5,5,5,5,5,5,5,5,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,9,1,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,1,1,0,0,0,1,0,1,0,0,0,1,0,0,0,0,0,1,0],
[ 0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,7,7,0,0,0,0,0,0,0,0,0,0,9,1,0,0,0,7,0,0,0,0,7,0,1,0,0,0,1,0,0,0,0,1,1,0],
[ 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,9,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,7,1,0],
[ 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,0,0,0,1,9,9,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,1,0],
[ 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,0,0,1,0],
[ 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1,8,8,8,8,8,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,0,0,0,1,0,0,0,1,1,1,0,0,0,1,0],
[ 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,7,7,0,0,0,1,0],
[ 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,0,0,0,1,0,0,0,0,0,1,0],
[ 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,3,0,1,0,0,0,0,0,0,0,0,0,0,1,5,5,5,5,5,5,5,5,5,5,5,5,1,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0],
[ 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,1,5,5,5,5,5,5,5,5,5,5,5,5,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,1,1,0],
[ 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0],
[ 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,0,0]]]


def dessiner_cotes_bloc_3d(fenetre, couleur, x, y, taille_bloc, profondeur, bloc):
    offset = profondeur // 2
    if bloc == 8:
        for i in range(profondeur):
            pos_x = x - i
            pos_y = y + i + taille_bloc
 
            if i < profondeur - 1:  
                pygame.draw.polygon(fenetre, couleur, [(pos_x, pos_y), (pos_x + taille_bloc, pos_y), (pos_x + taille_bloc // 2, pos_y - taille_bloc)])
    elif bloc == 7:
        for i in range(profondeur):
            pos_x = x - i + 7  
            pos_y = y + i -7
            if i < profondeur - 1:  
                pygame.draw.polygon(fenetre, couleur, [(pos_x, pos_y), (pos_x + taille_bloc, pos_y), (pos_x + taille_bloc // 2, pos_y + taille_bloc)])
    else : 
        for i in range(1, profondeur):
            taille = taille_bloc
            pos_x = x - offset + i
            pos_y = y + offset - i

            couleur_actuelle = couleur
            pygame.draw.rect(fenetre, couleur_actuelle, (pos_x, pos_y, taille, taille))

def dessiner_face_superieure_bloc_3d(fenetre, couleur_premiere_couche, x, y, taille_bloc, profondeur, bloc):
    taille = taille_bloc

    if bloc == 8:
        pos_x = x - profondeur   
        pos_y = y + profondeur  + taille_bloc

        pygame.draw.polygon(fenetre, couleur_premiere_couche, [(pos_x, pos_y), (pos_x + taille_bloc, pos_y), (pos_x + taille_bloc // 2, pos_y - taille_bloc)])
    elif bloc == 7:
        pos_x = x - profondeur  + 7
        pos_y = y + profondeur -7
        pygame.draw.polygon(fenetre, couleur_premiere_couche, [(pos_x, pos_y), (pos_x + taille_bloc, pos_y), (pos_x + taille_bloc // 2, pos_y + taille_bloc)])
    else :
        offset = profondeur // 2
        pos_x = x - offset
        pos_y = y + offset

        couleur_actuelle = couleur_premiere_couche
        pygame.draw.rect(fenetre, couleur_actuelle, (pos_x, pos_y, taille_bloc, taille_bloc))


def dessiner_plateformes(fenetre, niveau, taille_bloc, camera):
    profondeur = 13
    couleur_bloc = (218, 205, 229)
    couleur_premiere_couche = (218, 205, 229)

    blocs = []
    for i, ligne in enumerate(niveau):
        for j, bloc in enumerate(ligne):
            if bloc in {1, 2, 3, 4, 5, 7,8,9,10}:
                blocs.append((i, j, bloc))

    blocs.sort(key=lambda x: x[0])
    # (164, 155, 172)
    if niv_actu == 0:
        couleur = "#a7a753"
        couleur2 = "#777731"
        couleurbloc ="#5353a7"
        couleurbloc2 = "#323177"
    elif niv_actu == 1:
        couleur = "#8e84a4"
        couleur2 = "#3a314d"
        couleurbloc = "#9ba485"
        couleurbloc2 = "#444d32"
    elif niv_actu == 2:
        couleur = "#9ba485"
        couleur2 = "#255c48"
        couleurbloc = "#5c263a"
        couleurbloc2 = "#9a4061"

    
    for i, j, bloc in blocs:
        x = j * taille_bloc - camera.x
        y = i * taille_bloc - camera.y
        offset = 5 * math.sin(2 * math.pi * ((pygame.time.get_ticks() + j * 100) % 2000) / 2000)

        if bloc == 1:
            dessiner_cotes_bloc_3d(fenetre,couleurbloc, x, y, taille_bloc, profondeur, bloc)
        elif bloc == 2:
            dessiner_cotes_bloc_3d(fenetre, "#F38F0F", x, y, taille_bloc, profondeur, bloc)
        elif bloc == 3:
            dessiner_cotes_bloc_3d(fenetre, "#180D46", x, y, taille_bloc, profondeur, bloc)
        elif bloc == 4:
            dessiner_cotes_bloc_3d(fenetre, "#9333FF", x, y, taille_bloc, profondeur, bloc)
        elif bloc == 5:
            dessiner_cotes_bloc_3d(fenetre, couleur, x, y- offset, taille_bloc, profondeur, bloc)
        elif bloc == 6:
            offset_y = 50 * math.sin(2 * math.pi * (pygame.time.get_ticks() % 2000) / 2000)
            dessiner_cotes_bloc_3d(fenetre, couleurbloc, j * taille_bloc - camera.x, i * taille_bloc - camera.y + offset_y, taille_bloc, profondeur,bloc) 
        elif bloc == 8:

            dessiner_cotes_bloc_3d(fenetre,couleurbloc, x, y, taille_bloc *0.9, profondeur, bloc)
        elif bloc == 9:
            if (pygame.time.get_ticks() // 2000) % 2 == 0:
                dessiner_cotes_bloc_3d(fenetre,couleurbloc, x, y, taille_bloc, profondeur, bloc)
        elif bloc == 7:
            dessiner_cotes_bloc_3d(fenetre,couleurbloc, x, y, taille_bloc*0.9, profondeur, bloc)
    for i, j, bloc in blocs:
        x = j * taille_bloc - camera.x
        y = i * taille_bloc - camera.y
        offset = 5 * math.sin(2 * math.pi * ((pygame.time.get_ticks() + j * 100) % 2000) / 2000)

        if bloc == 1:
            dessiner_face_superieure_bloc_3d(fenetre, couleurbloc2, x, y, taille_bloc, profondeur, bloc)
        elif bloc == 2:
            dessiner_face_superieure_bloc_3d(fenetre, couleurbloc2, x, y, taille_bloc, profondeur, bloc)
        elif bloc == 3:
            dessiner_face_superieure_bloc_3d(fenetre, couleurbloc2, x, y, taille_bloc, profondeur, bloc)
        elif bloc == 4:
            dessiner_face_superieure_bloc_3d(fenetre, "#9333FF", x, y, taille_bloc, profondeur, bloc)        
        elif bloc == 5:
            dessiner_face_superieure_bloc_3d(fenetre, couleur, x, y- offset, taille_bloc, profondeur, bloc)
            dessiner_face_superieure_bloc_3d(fenetre, couleur2, x, y - offset, taille_bloc, profondeur, bloc)
        elif bloc == 6:
                offset_y = 50 * math.sin(2 * math.pi * (pygame.time.get_ticks() % 2000) / 2000)
                dessiner_face_superieure_bloc_3d(fenetre, couleurbloc2, j * taille_bloc - camera.x, i * taille_bloc - camera.y + offset_y, taille_bloc, profondeur, bloc)
        elif bloc == 8:
            dessiner_face_superieure_bloc_3d(fenetre, couleurbloc2, x, y, taille_bloc * 0.9, profondeur, bloc)
        elif bloc == 9:
            if (pygame.time.get_ticks() // 2000) % 2 == 0:    
                dessiner_face_superieure_bloc_3d(fenetre, couleurbloc2, x, y, taille_bloc, profondeur, bloc)
        elif bloc == 7:
            dessiner_face_superieure_bloc_3d(fenetre, couleurbloc2, x, y, taille_bloc*0.9, profondeur, bloc)

def generer_points_parabole(x0, y0, vx, vy, gravite, nb_points):
    points = []
    for t in range(nb_points):
        x = x0 + vx * t
        y = y0 - (vy * t - 0.5 * gravite * t ** 2)
        points.append((x, y))
    return points

def dessiner_parabole(fenetre, x0, y0, vx, vy, gravite, nb_points, couleur, camera):
    x, y = x0, y0
    for t in range(1, nb_points):
        x_prec, y_prec = x, y
        x += vx
        y += vy
        vy += gravite
        pygame.draw.line(fenetre, couleur, (x_prec-camera.x, y_prec- camera.y), (x-camera.x, y- camera.y))

#-----------------------------------------------------------
class ExplosionParticle:
    def __init__(self, x, y, size, speed, angle, color, lifespan):
        self.x = x
        self.y = y
        self.size = size
        self.speed = speed
        self.angle = angle
        self.color = color
        self.lifespan = lifespan

def generate_explosion_particles(niveau, taille_bloc, num_particles=8):
    explosion_particles = []
    for i, ligne in enumerate(niveau):
        for j, bloc in enumerate(ligne):
            if bloc == 6:
                x = j * taille_bloc + random.randint(0, taille_bloc)
                y = i * taille_bloc + random.randint(0, taille_bloc)
                for _ in range(num_particles):
                    size = random.randint(2, 5)
                    speed = random.uniform(1, 3)
                    angle = random.uniform(0, 2 * math.pi)
                    color = random.choice([(255, 0, 0), (255, 128, 0), (255, 255, 0)])
                    lifespan = random.randint(10, 30)
                    explosion_particle = ExplosionParticle(x, y, size, speed, angle, color, lifespan)
                    explosion_particles.append(explosion_particle)
    return explosion_particles

def update_explosion_particles(explosion_particles):
    for particle in explosion_particles:
        particle.x += particle.speed * math.cos(particle.angle)
        particle.y += particle.speed * math.sin(particle.angle)
        particle.lifespan -= 1
    return [particle for particle in explosion_particles if particle.lifespan > 0]

def draw_explosion_particles(fenetre, explosion_particles, camera):
    for particle in explosion_particles:
        particle_screen_x = int(particle.x - camera.x)
        particle_screen_y = int(particle.y - camera.y)
        pygame.draw.rect(fenetre, particle.color, pygame.Rect(particle_screen_x, particle_screen_y, particle.size, particle.size))
 
 
        
#------------------------------
explosion_particles = []     
trainee = []
couleurs_trainee = [(254, 108, 0), (236, 191, 7), (255, 168, 56), (255, 113, 56), (255, 77, 56), (255, 248, 31)]
tailles_particules = [2, 3, 4, 5, 6, 6]
duree_vie_particule = 20
nombre_particules = 3
clock = pygame.time.Clock()
gravite = 0.2
vitesse_lancer = 10
force_max = 200
camera = Camera(largeur, hauteur)
deplacement_actif = False
clic_initial = None
niveau_surface = pygame.Surface((largeur, hauteur), pygame.SRCALPHA)
personnage = Personnage(160, 650, 25)
trail_particles = []
trail_frequency = 2
frame_count = 0
scroll = 0
particles = []
water_particles = []
persoo_rect = pygame.Rect(personnage.x, personnage.y, personnage.taille, personnage.taille)


debut_course=time.time()



def traiter_deplacement(personnage, deplacement_actif, clic_initial, force_max, vitesse_lancer, gravite):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if not deplacement_actif:
                clic_initial = pygame.mouse.get_pos()
                deplacement_actif = True
            elif not personnage.sur_le_sol:
                personnage.vx *= 0.9
                personnage.vy *= 0.9

        if event.type == pygame.MOUSEBUTTONUP:
            if deplacement_actif:
                clic_final = pygame.mouse.get_pos()
                dx, dy = clic_final[0] - clic_initial[0], clic_initial[1] - clic_final[1]

                force = min(force_max, (dx ** 2 + dy ** 2) ** 0.5)
                angle = math.atan2(dy, dx)
                personnage.vx = -vitesse_lancer * math.cos(angle) * force / force_max
                personnage.vy = vitesse_lancer * math.sin(angle) * force / force_max
                deplacement_actif = False

    if deplacement_actif:
        position_courante = pygame.mouse.get_pos()
        dx, dy = position_courante[0] - clic_initial[0], clic_initial[1] - position_courante[1]
        force = min(force_max, (dx ** 2 + dy ** 2) ** 0.5)
        angle = math.atan2(dy, dx)

        vx = -vitesse_lancer * math.cos(angle) * force / force_max
        vy = vitesse_lancer * math.sin(angle) * force / force_max

        dessiner_parabole(fenetre, personnage.x + personnage.taille / 2, personnage.y + personnage.taille / 2, vx, vy, gravite, 50, "white", camera)
        charge_son.play()
    
    return deplacement_actif, clic_initial
def gerer_trainee(trainee, personnage, tailles_particules, couleurs_trainee, duree_vie_particule, nombre_particules):
    trainee.extend(creer_particules(personnage.x + 7, personnage.y + 7, tailles_particules, couleurs_trainee, duree_vie_particule, nombre_particules))
    for particule in trainee:
        particule.update()
        particule.draw(fenetre, camera)
    return [particule for particule in trainee if particule.duree_vie > 0]

def gerer_particles_eau(water_particles, niveau, taille_bloc, camera, generation_probability=0.0038):
    new_water_particles = generate_water_particles(niveau[niv_actu], taille_bloc, camera, generation_probability)
    water_particles.extend(new_water_particles)
    for particle in water_particles:
        particle.y -= particle.speed
    water_color = (48, 148, 191)
    for particle in water_particles:
        particle_screen_x = int(particle.x - camera.x)
        particle_screen_y = int(particle.y - camera.y)
        pygame.draw.rect(fenetre, "#9ba485", pygame.Rect(particle_screen_x, particle_screen_y, particle.size, particle.size))
    return [particle for particle in water_particles if particle.y > 0]

def gerer_particles_explosion(explosion_particles, niveau, taille_bloc):
    new_explosion_particles = generate_explosion_particles(niveau[niv_actu], taille_bloc)
    explosion_particles.extend(new_explosion_particles)
    explosion_particles = update_explosion_particles(explosion_particles)
    draw_explosion_particles(fenetre, explosion_particles, camera)
    return explosion_particles


# Créer une font
font = pygame.font.Font("ressources/altertype-Regular.otf", 36)
bg_menu = pygame.image.load("ressources/bg_menu.png")

def afficher_menu(pos_souris):
    
    fenetre.blit(bg_menu, (0, 0))
    jouer_text = font.render("Jouer", True, (255,255,255))  
    quitter_text = font.render("Quitter", True, (255,255,255))  
    
    jouer_rect = jouer_text.get_rect(center=((largeur/2), 150))  
    quitter_rect = quitter_text.get_rect(center=((largeur/2), 200))  

   
    if jouer_rect.collidepoint(pos_souris):
        jouer_text = font.render("Jouer", True, (255,165,0))  

    if quitter_rect.collidepoint(pos_souris):
        quitter_text = font.render("Quitter", True, (255,165,0))  

    fenetre.blit(jouer_text, jouer_rect)  
    fenetre.blit(quitter_text, quitter_rect)  
    pygame.display.flip() 
    return jouer_rect, quitter_rect  
def afficher_menu_niveaux(pos_souris):
    fenetre.blit(bg_menu, (0, 0))

    niv1s = read("mon_fichier.txt")
    niv2s = read(1)
    niv3s = read(2)
    niv4s= read(3)
    niv1_text = font.render("Niveau Intro", True, (255,255,255))
    niv2_text = font.render("Niveau 1", True, (255,255,255))
    niv3_text = font.render("Niveau 2", True, (255,255,255))
    niv4_text = font.render("Niveau 3", True, (255,255,255))
    niv1_score = font.render("Meilleur score : " + str(niv1s), True, (255,255,255))
    niv2_score = font.render("Meilleur score : " + str(niv2s), True, (255,255,255))
    niv3_score = font.render("Meilleur score : "+ str(niv3s) , True, (255,255,255))
    niv4_score = font.render("Meilleur score : "+ str(niv4s) , True, (255,255,255))


    niv1_rect = niv1_text.get_rect(center=((largeur/2), 100))
    niv2_rect = niv2_text.get_rect(center=((largeur/2), 150))
    niv3_rect = niv3_text.get_rect(center=((largeur/2), 200))
    niv4_rect = niv4_text.get_rect(center=((largeur/2), 250))


    if niv1_rect.collidepoint(pos_souris):
        niv1_text = font.render("Niveau Intro", True, (255,165,0))
        fenetre.blit(niv1_score, (200, 400))
    if niv2_rect.collidepoint(pos_souris):
        niv2_text = font.render("Niveau 1", True, (255,165,0))
        fenetre.blit(niv2_score, (200, 400))
    if niv3_rect.collidepoint(pos_souris):
        niv3_text = font.render("Niveau 2", True, (255,165,0))
        fenetre.blit(niv3_score, (200, 400))
    if niv4_rect.collidepoint(pos_souris):
        niv4_text = font.render("Niveau 3", True, (255,165,0))
        fenetre.blit(niv4_score, (200, 400))

    fenetre.blit(niv1_text, niv1_rect)
    fenetre.blit(niv2_text, niv2_rect)
    fenetre.blit(niv3_text, niv3_rect)
    fenetre.blit(niv4_text, niv4_rect)

    pygame.display.flip()  

    return niv1_rect, niv2_rect, niv3_rect, niv4_rect  




fontt = "ressources/altertype-Regular.otf"
bg_menu = pygame.image.load("ressources/bg_menu.png")
fenetre.blit(bg_menu, (0, 0))
running = True
menu_actif = True
niveaux_actif = False
jouer_rect, quitter_rect = None, None
niv1_rect, niv2_rect, niv3_rect = None, None, None
while running:

    pos_souris = pygame.mouse.get_pos()

    if menu_actif:
        jouer_rect, quitter_rect = afficher_menu(pos_souris)
    elif niveaux_actif:
        niv1_rect, niv2_rect, niv3_rect, niv4_rect = afficher_menu_niveaux(pos_souris)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if menu_actif:
                if jouer_rect.collidepoint(pos_souris):
                    menu_actif = False
                    niveaux_actif = True
                elif quitter_rect.collidepoint(pos_souris):
                    pygame.quit()
                    sys.exit()
            elif niveaux_actif:
                if niv1_rect.collidepoint(pos_souris):
                    niv_actu = 0
                    temps_debut = time.time()
                    elapsed_time = pygame.time.get_ticks() / 1000  

                    running = False  # On quitte la boucle principale
                elif niv2_rect.collidepoint(pos_souris):
                    niv_actu = 1
                    temps_debut = time.time()
                    elapsed_time = pygame.time.get_ticks() / 1000  

                    running = False  # On quitte la boucle principale
                elif niv3_rect.collidepoint(pos_souris):
                    niv_actu = 2
                    temps_debut = time.time()
                    elapsed_time = pygame.time.get_ticks() / 1000  

                    running = False  # On quitte la boucle principale
                elif niv4_rect.collidepoint(pos_souris):
                    niv_actu = 3
                    temps_debut = time.time()
                    elapsed_time = pygame.time.get_ticks() / 1000  

                    running = False  # On quitte la boucle principale


    pygame.display.flip()



debut_course=time.time()
while True:
    elapsedd_time = ((pygame.time.get_ticks() / 1000)) - elapsed_time
    debut_course=time.time()
    clock.tick(60)
    scroll -= personnage.vx
    bg_images = []
    for i in range(1, 6):
            bg_image = pygame.image.load(f"ressources/bg/{niv_actu}/{i}.png").convert_alpha()
            bg_images.append(bg_image)
            bg_width = bg_images[0].get_width()
    draw_bg()
    dessiner_plateformes(fenetre, niveau[niv_actu], taille_bloc, camera)

    if personnage.sur_le_sol:
        deplacement_actif, clic_initial = traiter_deplacement(personnage, deplacement_actif, clic_initial, force_max, vitesse_lancer, gravite)

    trainee = gerer_trainee(trainee, personnage, tailles_particules, couleurs_trainee, duree_vie_particule, nombre_particules)
    water_particles = gerer_particles_eau(water_particles, niveau, taille_bloc, camera)
    explosion_particles = gerer_particles_explosion(explosion_particles, niveau, taille_bloc)

    personnage.maj_vitesse(gravite)
    personnage.deplacer(personnage.vx, personnage.vy)
    personnage.collision(taille_bloc)
        
    if not personnage.sur_le_sol:
            camera.update(personnage)
    personnage.dessiner(fenetre, camera)


    if personnage.sur_le_sol:
            personnage.vx *= 0.2
            if abs(personnage.vx) < 0.1:
                personnage.vx = 0
        
    
    font = pygame.font.Font("ressources/altertype-Regular.otf", 35) 

    texxt = font.render(f'{elapsedd_time:.1f}', True, (255, 255, 255))

    fenetre.blit(texxt, (largeur/2, 20))  

        
    text = font.render("❤"*personnage.vie, False, "red")
    fenetre.blit(text, (500, 20))
    pygame.display.flip()
    

