import re
def text_to_html(content: str) -> str:
    """
    Converts plain text into structured HTML without a system prompt.
    Detects headings, bullet points, and line breaks.
    """
    content = content.strip()

    # Convert headings (detect lines with all caps as headings)
    content = re.sub(r'(?m)^([A-Z ]+)$', r'<h2>\1</h2>', content)

    # Convert bullet points (- or *) to <ul><li>
    content = re.sub(r'(?m)^[-*]\s+(.*)$', r'<li>\1</li>', content)
    content = re.sub(r'(?s)(<li>.*?</li>)+', r'<ul>\g<0></ul>', content)

    # Convert inline code (words inside `backticks`) to <code>
    content = re.sub(r'`([^`]+)`', r'<code>\1</code>', content)

    # Convert line breaks to <br> for better readability
    content = content.replace("\n", "<br>")

    return f"""
    <html>
    <head><title>AI Response</title></head>
    <body>
        <div style="font-family: Arial, sans-serif; line-height: 1.6; padding: 20px;">
            {content}
        </div>
    </body>
    </html>
    """



prompt = """In the realm where twilight kisses dawn,
Amidst the dew-kissed blades of grass,
Where whispers of the night are softly drawn,
There lies a world where day and night amass.

Glitters dance upon the gentle streams,
Each ripple catching hints of sunlit gold,
Mirroring the dreams within our dreams,
Stories of the ancients quietly retold.

In fields of silver lined with hints of blue,
The stars descend like sequins from the skies,
Painting the horizon with a radiant hue,
As if the heavens blink with countless eyes.

Each speck of light a promise from afar,
A whisper carried on the evening breeze,
The cosmos beckons with the charm of stars,
Unveiling mysteries with such graceful ease.

Yet in the heart of this resplendent show,
We find that glitter is not all it seems,
A fleeting sparkle in the ebb and flow,
Mirrors life’s ephemeral bursts and beams.

For hidden in the static gleam of time,
Lies beauty found in moments, small and bright,
A spark of warmth, a melody, a chime,
Guiding us through shadows towards the light.

So as the glitters weave their golden thread,
And starlight graces every tear and smile,
Remember how the simplest joys are fed,
By gentle glimmers glowing all the while."""
response  = text_to_html(prompt)
print(response)