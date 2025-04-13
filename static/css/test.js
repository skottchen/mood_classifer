
const moodColorMap = {
    "Calm":           ["#88BDBC", "#C9E4DE", "#EEF6F6"],
    "Cool":           ["#5D7285", "#A3D2CA", "#DDE9F4"],
    "Dark":           ["#1C1C1C", "#4B4B4B", "#000000"],
    "Deep":           ["#132A3E", "#28536B", "#0A1E2F"],
    "Dramatic":       ["#720026", "#CE4257", "#FFF0F3"],
    "Dream":          ["#CBAACB", "#FFC8DD", "#F0E5F9"],
    "Emotional":      ["#6A4E77", "#DCA3BC", "#F5E9F1"],
    "Energetic":      ["#F72585", "#B5179E", "#FFEDF9"],
    "Fun":            ["#FFB703", "#F72585", "#FFFBE7"],
    "Funny":          ["#FFB4A2", "#FF99C8", "#FFE5EC"],
    "Groovy":         ["#CB997E", "#DDC9B4", "#FFE8D6"],
    "Happy":          ["#FFD60A", "#FFADAD", "#FFF9E3"],
    "Heavy":          ["#2C2C2C", "#FF5C5C", "#1A1A1A"],
    "Hopeful":        ["#92C7CF", "#AAD9BB", "#E5FDD1"],
    "Inspiring":      ["#FFD6A5", "#FDFFB6", "#FFFFF0"],
    "Love":           ["#F4ACB7", "#FFCAD4", "#FFF0F3"],
    "Meditative":     ["#D2F6C5", "#AED9E0", "#F0F9F9"],
    "Melancholic":    ["#556270", "#4ECDC4", "#E0F7FA"],
    "Mellow":         ["#FFE0AC", "#FFD3B4", "#FAF3DD"],
    "Melodic":        ["#B5EAD7", "#C7CEEA", "#EDF6F9"],
    "Motivational":   ["#F9DC5C", "#FF6F59", "#FCEADE"],
    "Positive":       ["#DFFFD6", "#F3FFE3", "#FBFFF1"],
    "Powerful":       ["#231942", "#5E548E", "#E0E0F8"],
    "Relaxing":       ["#A8DADC", "#F1FAEE", "#E0F7FA"],
    "Romantic":       ["#F4ACB7", "#FFCAD4", "#FFF0F3"],
    "Sad":            ["#6C757D", "#A6B1C3", "#D6DCE5"],
    "Sexy":           ["#800020", "#FF007F", "#FFF0F5"],
    "Slow":           ["#2B2D42", "#8D99AE", "#EDF2F4"],
    "Soft":           ["#F7E1D7", "#D6CFCB", "#F5F5F5"],
    "Upbeat":         ["#FF9F1C", "#FFBF69", "#FFF3C7"],
    "Uplifting":      ["#FFD6A5", "#C4FFF9", "#FDFFB6"]
  };
  

document.addEventListener('DOMContentLoaded', function () {
    const moodButton = document.querySelector('.submit_button');
    moodButton.addEventListener('click', function() {
        console.log("Button clicked!");
        applyMoodColors();
    });


    // Resize canvas if the window is resized
    window.addEventListener('resize', resizeCanvas);
    resizeCanvas(); // Call once initially to set the correct canvas size
});


function applyMoodColors() {
    const spotifyLink = document.getElementById("spotifyInput").value;
    document.getElementById('mood-header').textContent = 'Your song link is: ' + spotifyLink;
}




    const colors = moodColorMap[selectedMood];
    const contrastColor = getContrastingColor(colors[0]);
    document.getElementById('mood-header').style.color = contrastColor
    document.getElementById('songsList').style.color = contrastColor
    document.getElementById('moodText').style.color = contrastColor
   
   


    // If no colors found for mood, exit early
    if (!colors) {
      console.warn("Mood not found:", selectedMood);
      return;
    }


    // Blend the colors onto the canvas
    blendPaint(colors);



// Resize the canvas to full viewport size
function resizeCanvas() {
    const canvas = document.getElementById('paintCanvas');
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
}


// Blend the colors onto the canvas
function blendPaint(colors) {
    const canvas = document.getElementById('paintCanvas');
    const ctx = canvas.getContext('2d');


    // Create a linear gradient that blends the colors smoothly
    const gradient = ctx.createLinearGradient(0, 0, canvas.width, canvas.height);


    // Add color stops to the gradient
    gradient.addColorStop(0, colors[0]);
    gradient.addColorStop(0.5, colors[1]);
    gradient.addColorStop(1, colors[2]);


    // Apply the gradient to the entire canvas
    ctx.fillStyle = gradient;
    ctx.fillRect(0, 0, canvas.width, canvas.height);
}


function getContrastingColor(hexColor) {
    // Remove # if present
    hexColor = hexColor.replace("#", "");
 
    // Parse r, g, b values
    const r = parseInt(hexColor.substr(0, 2), 16);
    const g = parseInt(hexColor.substr(2, 2), 16);
    const b = parseInt(hexColor.substr(4, 2), 16);
 
    // Calculate luminance
    const luminance = (0.299 * r + 0.587 * g + 0.114 * b);
 
    // Return black or white based on luminance
    return luminance > 186 ? "#000000" : "#ffffff";
  }
 




