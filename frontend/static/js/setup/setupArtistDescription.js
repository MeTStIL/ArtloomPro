export async function setupArtisDescription(description) {
    const artistDescription = document.getElementById('artist-description');
    const descriptionSection = document.getElementById('description-section');
    if (description) {
        artistDescription.textContent = description;
        artistDescription.classList.remove('hidden');
        descriptionSection.classList.remove('hidden');
    }
}