import pygame

class Tutorial:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font("pixeboy.ttf", 30)
        self.button_font = pygame.font.Font("pixeboy.ttf", 40)

        # Diviser le tutoriel en plusieurs pages
        self.pages = [
            "Bienvenue dans EPSImester !",
            "Tu es un etudiant chez EPSI. Prepare-toi a affronter la realite de la vie etudiante.",
            "Chaque semaine, tu devras rendre un projet pour valider ton annee.",
            "Surveille ta barre d'energie et de morale pour ne pas te laisser deborder.",
            "Chaque jour, tu auras 5 actions a accomplir et 2 evenements aleatoires.",
            "Pour t'aider, tu peux utiliser des objets de ton inventaire. Accede a l'inventaire avec 'I'.",
            "Chaque mercredi, visite le magasin pour acheter des objets rares et utiles.",
            "Bonne chance et amuse-toi bien !"
        ]

        # Ajouter des images specifiques aux pages
        self.images = [
            None,  # Pas d'image pour la page 0
            None,  # Pas d'image pour la page 1
            None,  # Pas d'image pour la page 2
            [pygame.image.load("Data/Sprites/bar_energy.png"), pygame.image.load("Data/Sprites/bar_moral.png")],
            None,  # Pas d'image pour la page 3
            None,  # Pas d'image pour la page 5
            None,  # Pas d'image pour la page 6
            None   # Pas d'image pour la page 7
        ]

        self.current_page = 0
        self.running = True
        self.button_rect = pygame.Rect(0, 0, 200, 50)  # Initialisation du bouton

    def draw_button(self):
        # Dessiner le bouton
        button_color = (0, 128, 255)
        button_hover_color = (0, 255, 255)
        text_color = (255, 255, 255)

        mouse_pos = pygame.mouse.get_pos()
        if self.button_rect.collidepoint(mouse_pos):
            pygame.draw.rect(self.screen, button_hover_color, self.button_rect)
        else:
            pygame.draw.rect(self.screen, button_color, self.button_rect)

        button_text = self.button_font.render("Suivant", True, text_color)
        text_rect = button_text.get_rect(center=self.button_rect.center)
        self.screen.blit(button_text, text_rect)

    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.button_rect.collidepoint(event.pos):
                self.current_page += 1
                if self.current_page >= len(self.pages):
                    self.running = False

    def draw(self):
        self.screen.fill((0, 0, 0))  # Fond noir

        # Afficher les images si elles existent
        images = self.images[self.current_page]
        if images:
            # Positionner les images
            if len(images) > 0:
                image1 = images[0]
                image1_rect = image1.get_rect(center=(self.screen.get_width() // 3, 200))  # Ajustez la position pour la premiere image
                self.screen.blit(image1, image1_rect)

            if len(images) > 1:
                image2 = images[1]
                image2_rect = image2.get_rect(center=(2 * self.screen.get_width() // 3, 200))  # Ajustez la position pour la deuxieme image
                self.screen.blit(image2, image2_rect)

        # Afficher le texte sous les images
        text_surface = self.font.render(self.pages[self.current_page], True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 + 0))  # Ajustez la distance entre les images et le texte
        self.screen.blit(text_surface, text_rect)

        # Positionner le bouton en bas de l'ecran
        self.button_rect.center = (self.screen.get_width() // 2, self.screen.get_height() - 100)
        self.draw_button()

        pygame.display.flip()
