import cv2
import pyautogui
import pyaudio
import wave
import os

try:
    import art
except ImportError:
    os.system("pip install art")
    os.system("pip3 install art")
    import art

art.tprint("SeeWare")

def take_screenshot(file_name):
    # Capture screenshot of the entire screen
    screenshot = pyautogui.screenshot()
    screenshot.save(file_name)
    print("Screenshot saved as", file_name)

def take_photo(file_name):
    # Capture video from facecam
    facecam = cv2.VideoCapture(0)
    ret, frame = facecam.read()
    if ret:
        cv2.imwrite(file_name, frame)
        print("Photo captured and saved as", file_name)
    else:
        print("Error capturing photo")

def record_audio(file_name, duration):
    # Record audio
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1  # Change this to 1
    RATE = 44100
    RECORD_SECONDS = duration

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    frames = []
    total_frames = int(RATE / CHUNK * RECORD_SECONDS)

    print("Recording...")

    for _ in range(total_frames):
        frames.append(stream.read(CHUNK))

    print("Finished recording.")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(file_name, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    print("Audio saved as", file_name)

def main():
    # Take screenshot of the desktop
    take_screenshot("desktop_screenshot.png")

    # Take photo using facecam
    take_photo("facecam_photo.png")

    duration = int(input("Enter the seconds to record: "))
    # Record audio
    record_audio("recorded_audio.wav", duration + 1)

    # Release video captures
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()