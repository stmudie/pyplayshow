import os
import pygame
from time import sleep

class pyplayshow :
    screen = None;
    
    def __init__(self):
        "Ininitializes a new pygame screen using the framebuffer"
        # Based on "Python GUI in Linux frame buffer"
        # http://www.karoltomala.com/blog/?p=679
        pygame.init()
        disp_no = os.getenv("DISPLAY")
        if disp_no:
            print "I'm running under X display = {0}".format(disp_no)
        
        # Check which frame buffer drivers are available
        # Start with fbcon since directfb hangs with composite output
        drivers = ['fbcon', 'directfb', 'svgalib']
        found = False
        for driver in drivers:
            # Make sure that SDL_VIDEODRIVER is set
            if not os.getenv('SDL_VIDEODRIVER'):
                os.putenv('SDL_VIDEODRIVER', driver)
            try:
                pygame.display.init()
            except pygame.error:
                print 'Driver: {0} failed.'.format(driver)
                continue
            found = True
            break
    
        if not found:
            raise Exception('No suitable video driver found!')
        
        size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
        print "Framebuffer size: %d x %d" % (size[0], size[1])
        self.screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
        # Clear the screen to start
        self.background=((100,100,100))
        self.screen.fill(self.background)       
        # Initialise font support
        pygame.font.init()
        self.font = pygame.font.Font(None, 600)
        # Render the screen
        pygame.display.update()
        # Init the mixer
        pygame.mixer.quit()
        pygame.mixer.init(44100)
        

    def __del__(self):
        "Destructor to make sure pygame shuts down, etc."

    def play(self, soundfile, noplay = False):
        sound = pygame.mixer.Sound('soundfile')
        if not noplay: sound.play()
        return sound

    def setbackground(self,background=''):
        if background != '':
            self.background = background
        self.screen.fill(self.background)

    def show(self, text, colour = (200,200,200), background='', time=5):
        self.setbackground(background)
        text_surface = self.font.render(text, True, colour)
        self.screen.blit(text_surface,(300,300))
        pygame.display.update()
        if time != 0:
            sleep(time)
            self.setbackground()
            pygame.display.update()
