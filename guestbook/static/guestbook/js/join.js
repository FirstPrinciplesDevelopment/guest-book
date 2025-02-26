window.onload = async function () {

    let shuffleNameButton = document.getElementById("shuffle-name-button");
    let nameInput = document.getElementById("name-input");

    // Set input to first pair.
    nameInput.value = await getRandomName()

    shuffleNameButton.addEventListener("click", async function () {
        randomName = await getRandomName();
        nameInput.value = randomName;
    });

    async function getRandomName() {
        const url = "/name/";
        try {
            const response = await fetch(url);
            if (!response.ok) {
                throw new Error(`Response status: ${response.status}`);
            }

            const json = await response.json();
            return json.name;

        } catch (error) {
            console.error(error.message);
        }
    }

};
