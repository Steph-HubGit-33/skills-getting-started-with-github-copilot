document.addEventListener("DOMContentLoaded", () => {
  const activitiesList = document.getElementById("activities-list");
  const activitySelect = document.getElementById("activity");
  const signupForm = document.getElementById("signup-form");
  const messageDiv = document.getElementById("message");

  // Fonction pour récupérer les activités depuis l'API
  async function fetchActivities() {
    try {
      const response = await fetch("/activities");
      const activities = await response.json();

      // Effacer le message de chargement
      activitiesList.innerHTML = "";

      // Remplir la liste des activités
      Object.entries(activities).forEach(([name, details]) => {
        const activityCard = document.createElement("div");
        activityCard.className = "activity-card";

        const spotsLeft = details.max_participants - details.participants.length;

        activityCard.innerHTML = `
          <h4>${name}</h4>
          <p>${details.description}</p>
          <p><strong>Horaire :</strong> ${details.horaire}</p> <!-- Utilise "horaire" -->
          <p><strong>Disponibilité :</strong> ${spotsLeft} places restantes</p>
          <p><strong>Participants :</strong></p>
          <ul class="participants-list">
            ${details.participants.map(participant => `<li>${participant}</li>`).join("")}
          </ul>
        `;

        activitiesList.appendChild(activityCard);

        // Ajouter une option au menu déroulant
        const option = document.createElement("option");
        option.value = name;
        option.textContent = name;
        activitySelect.appendChild(option);
      });
    } catch (error) {
      activitiesList.innerHTML = "<p>Échec du chargement des activités. Veuillez réessayer plus tard.</p>";
      console.error("Erreur lors de la récupération des activités :", error);
    }
  }

  // Gérer la soumission du formulaire
  signupForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const email = document.getElementById("email").value;
    const activity = document.getElementById("activity").value;

    try {
      const response = await fetch(
        `/activities/${encodeURIComponent(activity)}/signup?email=${encodeURIComponent(email)}`,
        {
          method: "POST",
        }
      );

      const result = await response.json();

      if (response.ok) {
        messageDiv.textContent = result.message;
        messageDiv.className = "success";
        signupForm.reset();

        // Rafraîchir dynamiquement la liste des activités et des participants
        await fetchActivities();
      } else {
        messageDiv.textContent = result.detail || "Une erreur s'est produite";
        messageDiv.className = "error";
      }

      messageDiv.classList.remove("hidden");

      // Masquer le message après 5 secondes
      setTimeout(() => {
        messageDiv.classList.add("hidden");
      }, 5000);
    } catch (error) {
      messageDiv.textContent = "Échec de l'inscription. Veuillez réessayer.";
      messageDiv.className = "error";
      messageDiv.classList.remove("hidden");
      console.error("Erreur lors de l'inscription :", error);
    }
  });

  // Initialiser l'application
  fetchActivities();
});
