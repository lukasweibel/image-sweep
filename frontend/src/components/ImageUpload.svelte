<script>
  let files = [];
  let fileUrls = [];
  let fileMessages = [];

  function handleFileChange(event) {
    files = Array.from(event.target.files);
    fileUrls = files.map((file) => URL.createObjectURL(file));
    fileMessages = files.map(() => "");
  }

  async function uploadFiles() {
    if (files.length === 0) {
      alert("Please select at least one file first.");
      return;
    }

    for (let i = 0; i < files.length; i++) {
      const file = files[i];
      const formData = new FormData();
      formData.append("picture", file);

      try {
        const response = await fetch("/picture", {
          method: "POST",
          body: formData,
        });

        if (response.ok) {
          const result = await response.json();
          fileMessages[i] = result.message;
        } else {
          const error = await response.text();
          fileMessages[i] = "Error uploading file: " + error;
        }
      } catch (error) {
        fileMessages[i] = "Error uploading file: " + error.message;
      }
    }
  }

  function downloadOthers() {
    const zip = new JSZip();

    files.forEach((file, index) => {
      if (fileMessages[index] === "other") {
        zip.file(file.name, file);
      }
    });

    zip.generateAsync({ type: "blob" }).then(function (content) {
      saveAs(content, "others.zip");
    });
  }
</script>

<div class="upload-container">
  <input type="file" accept="image/*" multiple on:change={handleFileChange} />

  <button on:click={uploadFiles}>Classify</button>
  <p>
    This button will download as a ZIP-Folder all pictures which are not
    classified as screenshots
  </p>
  <button on:click={downloadOthers}>Download Others</button>
</div>

<div class="grid-container">
  {#each fileUrls as url, i}
    <div class="grid-item">
      <p>{fileMessages[i]}</p>
      <img src={url} alt="Selected image" />
    </div>
  {/each}
</div>

<style>
  .upload-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-top: 20px;
  }

  .upload-container input {
    margin-bottom: 10px;
  }

  .grid-container {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(100px, 1fr));
    gap: 10px;
    margin-top: 20px;
  }

  .grid-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    border: 1px solid #ccc;
    padding: 5px;
  }

  .grid-item img {
    max-width: 100%;
    max-height: 100px;
    object-fit: cover;
  }

  .grid-item p {
    margin: 0;
    padding: 5px;
    text-align: center;
    font-size: 12px;
    color: #333;
  }
</style>
