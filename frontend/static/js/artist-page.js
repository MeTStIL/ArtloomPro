import { fetchArtistById } from "./fetchArtistById.js"
import { fetchPaintingById} from "./fetchPaintingById.js";


async function fetchData(artistPageId) {
    try {
        const response = await fetch(`http://127.0.0.1:8000/artist_pages/${artistPageId}`);

        const data = await response.json();
        const artistInfoDiv = document.getElementById('artist-info');

        const url = data.url;
        const id = data.artist_id;
        const paintingsIds = data.painting_ids;


        const artistInfo = await fetchArtistById(id);

        if (artistInfo) {
            artistInfoDiv.innerHTML = `
                <p>ArtistName: ${artistInfo.name}</p>
                <p>Nsme: ${artistInfo.name}</p>
                <img src="${artistInfo.img_url}" alt="Artist Image" style="max-width: 300px; height: auto;">
                <p>Contacts: ${artistInfo.contacts}</p>
                <p>Description: ${artistInfo.description}</p>
            `;
        }

        const paintingInfoDiv = document.getElementById('paintings-info')

        for (const paintingId of paintingsIds)
        {
             const paintingInfo = await fetchPaintingById(paintingId)
             paintingInfoDiv.innerHTML += `
             <p>Title: ${paintingInfo.title}</p>
             <img src="${paintingInfo.img_url}" alt="Painting" style="max-width: 300px; height: auto;">
             <p>Year: ${paintingInfo.year}</p>
             <p>Description: ${paintingInfo.description} </p>`
        }

    } catch (error) {
        console.error("Ошибка при выполнении запроса:", error);

        const result = document.getElementById('artist-page');
        if (result) {
            result.innerHTML = "<p>Ошибка при загрузке данных.</p>";
        }
    }
}

const path = window.location.pathname;
const artistPageId = path.split("/").pop();

document.addEventListener("DOMContentLoaded", () => fetchData(artistPageId));


