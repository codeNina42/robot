import pygame
import speech_recognition as sr
import pyttsx3
import threading
import time

pygame.init()
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Voice Controlled Robot")
clock = pygame.time.Clock()

# Robot position
cx, cy = 320, 240
left_arm_offset = 0
right_arm_offset = 0
left_leg_offset = 0
right_leg_offset = 0
head_offset = 0

running = True
robot_running = False

# Voice engine
engine = pyttsx3.init()
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Voice recognition
def listen_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎙️ Say a command...")
        audio = r.listen(source)
        try:
            command = r.recognize_google(audio).lower()
            print("🗣️ You said:", command)
            return command
        except:
            print("❌ Sorry, I didn't catch that.")
            return ""

# Auto-run leg movement
def auto_run():
    global left_leg_offset, right_leg_offset, robot_running
    step = 1
    while robot_running:
        left_leg_offset += 10 * step
        right_leg_offset -= 10 * step
        if abs(left_leg_offset) > 30:
            step *= -1
        time.sleep(0.2)

speak("Hello, I am your robot. Give me a command!")

# Background thread for voice commands
def voice_thread():
    global running, left_arm_offset, right_arm_offset
    global left_leg_offset, right_leg_offset, head_offset, robot_running

    while running:
        command = listen_command()

        # Hands
        if "left hand up" in command:
            left_arm_offset -= 10
            speak("Left hand up")
        elif "left hand down" in command:
            left_arm_offset += 10
            speak("Left hand down")
        elif "right hand up" in command:
            right_arm_offset -= 10
            speak("Right hand up")
        elif "right hand down" in command:
            right_arm_offset += 10
            speak("Right hand down")

        # Legs
        elif "left leg up" in command:
            left_leg_offset -= 10
            speak("Left leg up")
        elif "left leg down" in command:
            left_leg_offset += 10
            speak("Left leg down")
        elif "right leg up" in command:
            right_leg_offset -= 10
            speak("Right leg up")
        elif "right leg down" in command:
            right_leg_offset += 10
            speak("Right leg down")

        # Head
        elif "head up" in command:
            head_offset -= 10
            speak("Head up")
        elif "head down" in command:
            head_offset += 10
            speak("Head down")

        # Running
        elif "run" in command and not robot_running:
            robot_running = True
            threading.Thread(target=auto_run, daemon=True).start()
            speak("Robot is running")
        elif "stop run" in command:
            robot_running = False
            left_leg_offset = right_leg_offset = 0
            speak("Robot stopped running")

        # Stop program
        elif "stop" in command:
            speak("Stopping program")
            running = False
            break

# Start voice listener
threading.Thread(target=voice_thread, daemon=True).start()

# Main drawing loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((30, 30, 30))

    # Head
    pygame.draw.rect(screen, (200, 200, 200), (cx - 40, cy - 120 + head_offset, 80, 80))
    pygame.draw.circle(screen, (0, 0, 0), (cx - 20, cy - 90 + head_offset), 5)
    pygame.draw.circle(screen, (0, 0, 0), (cx + 20, cy - 90 + head_offset), 5)
    pygame.draw.line(screen, (0, 0, 0), (cx - 25, cy - 70 + head_offset), (cx + 25, cy - 70 + head_offset), 3)

    # Body
    pygame.draw.rect(screen, (100, 150, 220), (cx - 60, cy - 40, 120, 160))

    # Arms (left, right)
    pygame.draw.rect(screen, (180, 100, 100), (cx - 100, cy - 40 + left_arm_offset, 40, 100))
    pygame.draw.rect(screen, (180, 100, 100), (cx + 60, cy - 40 + right_arm_offset, 40, 100))

    # Legs (left, right)
    pygame.draw.rect(screen, (120, 180, 120), (cx - 40, cy + 120 + left_leg_offset, 30, 100))
    pygame.draw.rect(screen, (120, 180, 120), (cx + 10, cy + 120 + right_leg_offset, 30, 100))

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
