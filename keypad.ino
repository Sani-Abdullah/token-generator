#include <Keypad.h>

const byte ROWS = 4; // four rows
const byte COLS = 3; // three columns

char keys[ROWS][COLS] = {
    {'1', '2', '3'},
    {'4', '5', '6'},
    {'7', '8', '9'},
    {'*', '0', '#'}};

byte rowPins[ROWS] = {5, 4, 3, 2}; // connect to the row pinouts of the keypad
byte colPins[COLS] = {8, 7, 6};    // connect to the column pinouts of the keypad

Keypad keypad = Keypad(makeKeymap(keys), rowPins, colPins, ROWS, COLS);

int ledPin = 13;
const int inputMaxLength = 20;
int cursorPosition = 0;
char input_buffer[inputMaxLength];

void setup()
{
    Serial.begin(9600);
    keypad.addEventListener(keypadEvent);
    pinMode(ledPin, OUTPUT);
}

void loop()
{
    char key = keypad.getKey();
    if (key)
    {
        // Serial.println(key);
    }
}

void keypadEvent(KeypadEvent key)
{
    switch (keypad.getState())
    {
    case PRESSED:
        if (key == '*')
        {
            if (strlen(input_buffer) >= 1)
                input_buffer[strlen(input_buffer) - 1] = '\0';
            Serial.println(input_buffer);
        }
        else if (key == '#')
        {
            digitalWrite(ledPin, HIGH);
            delay(1000);
            digitalWrite(ledPin, LOW);
        }
        else
        {
            // Serial.println("=========");
            // strncat(input_buffer, &key, 140);
            // Serial.println(strlen(input_buffer));
            // Serial.println("=========");
            input_buffer[cursorPosition] = key;
            Serial.println(input_buffer);
            cursorPosition++;
        }
        break;

    case RELEASED:
        // digitalWrite(ledPin, LOW);
        break;

    case HOLD:
        Serial.println("HELD");
        break;
    }
}