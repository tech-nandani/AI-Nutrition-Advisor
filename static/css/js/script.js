document.addEventListener("DOMContentLoaded", function () {

    const chatBox = document.getElementById("chatBox");
    const userMessage = document.getElementById("userMessage");
    const sendButton = document.getElementById("sendButton");
    const quickQuestions = document.querySelectorAll(".quick-question");


    // Check chatbot elements exist
    if (!chatBox || !userMessage || !sendButton) {
        return;
    }


    // Send button
    sendButton.addEventListener("click", function () {
        sendMessage();
    });


    // Enter key
    userMessage.addEventListener("keydown", function (event) {

        if (event.key === "Enter") {
            event.preventDefault();
            sendMessage();
        }

    });


    // Quick question buttons
    quickQuestions.forEach(function (button) {

        button.addEventListener("click", function () {

            userMessage.value = button.textContent.trim();

            sendMessage();

        });

    });


    function sendMessage() {

        const message = userMessage.value.trim();


        // Empty message
        if (message === "") {
            return;
        }


        // Create user message
        const userChat = document.createElement("div");

        userChat.className = "chat-message user-message";

        userChat.innerHTML = `
            <div class="message-content">
                <strong>You</strong>
                <p>${message}</p>
            </div>
        `;


        chatBox.appendChild(userChat);


        // Clear input
        userMessage.value = "";


        // Scroll down
        chatBox.scrollTop = chatBox.scrollHeight;


        // Bot response after small delay
        setTimeout(function () {

            const botChat = document.createElement("div");

            botChat.className = "chat-message bot-message";


            const reply = getBotResponse(message);


            botChat.innerHTML = `
                <div class="bot-icon">
                    🤖
                </div>

                <div class="message-content">
                    <strong>AI Nutrition Assistant</strong>
                    <p>${reply}</p>
                </div>
            `;


            chatBox.appendChild(botChat);


            // Scroll down again
            chatBox.scrollTop = chatBox.scrollHeight;


        }, 500);

    }


    function getBotResponse(message) {

        const text = message.toLowerCase();


        if (
            text.includes("weight loss") ||
            text.includes("lose weight")
        ) {

            return "For healthy weight loss, focus on vegetables, fruits, lean protein, whole grains and regular physical activity. Try to reduce excessive sugary and processed foods.";

        }


        if (
            text.includes("protein")
        ) {

            return "Good high-protein vegetarian foods include paneer, tofu, lentils, chickpeas, kidney beans, Greek yogurt, soybeans and nuts.";

        }


        if (
            text.includes("water") ||
            text.includes("drink")
        ) {

            return "Most people need around 2 to 3 litres of water daily. Your exact requirement can change depending on your activity level and weather.";

        }


        if (
            text.includes("breakfast")
        ) {

            return "A healthy breakfast can include oats with fruits, poha with vegetables, eggs with whole-grain toast, or yogurt with nuts and fruits.";

        }


        if (
            text.includes("weight gain") ||
            text.includes("gain weight")
        ) {

            return "For healthy weight gain, include calorie-rich but nutritious foods such as bananas, milk, nuts, rice, potatoes, paneer and protein-rich meals.";

        }


        if (
            text.includes("calorie") ||
            text.includes("calories")
        ) {

            return "Your calorie needs depend on age, height, weight, gender and activity level. You can use your profile information for a more personalized recommendation.";

        }


        return "Great question! 🥗 A balanced diet should include vegetables, fruits, proteins, whole grains and healthy fats. Tell me more about your specific health or nutrition goal.";

    }

});