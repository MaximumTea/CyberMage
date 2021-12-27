from typing import Optional

from actions import Action, EscapeAction, MovementAction

import pygame
import sys


class EventDispatch:
    """This class dispatches events to methods depending on the type of event
        Based on libtcod event dispatch class"""
    def dispatch(self, event):
        if event.type == pygame.KEYDOWN:
            return self.ev_keydown(event)
        elif event.type == pygame.QUIT:
            return self.ev_quit(event)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            return self.ev_mousebuttondown(event)

    def ev_keydown(self, event):
        """Called when a keyboard button is pressed down."""

    def ev_quit(self, event):
        """Called when a quit event is triggered."""

    def ev_mousebuttondown(self, event):
        """Called when a mouse button is pressed."""

class EventHandler(EventDispatch):
    """This is a base object that is able to connect events to actions."""
    def ev_quit(self, event) -> Optional[Action]:
        pygame.quit()
        sys.exit()

    def ev_keydown(self, event) -> Optional[Action]:
        action = None
        key = event.key

        if key == pygame.K_KP9:
            action = MovementAction(dx = 0, dy = -1)
        if key == pygame.K_KP8:
            action = MovementAction(dx = -1, dy = -1)
        if key == pygame.K_KP7:
            action = MovementAction(dx = -1, dy = 0)
        if key == pygame.K_KP4:
            action = MovementAction(dx = -1, dy = 1)
        if key == pygame.K_KP1:
            action = MovementAction(dx = 0, dy = 1)
        if key == pygame.K_KP2:
            action = MovementAction(dx = 1, dy = 1)
        if key == pygame.K_KP3:
            action = MovementAction(dx = 1, dy = 0)
        if key == pygame.K_KP6:
            action = MovementAction(dx = 1, dy = -1)
        if key == pygame.K_ESCAPE:
            action = EscapeAction()
        return action
