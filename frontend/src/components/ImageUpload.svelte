<script>
  let file;

  async function uploadFile() {
    if (!file) {
      alert("Please select a file first.");
      return;
    }

    const formData = new FormData();
    formData.append("picture", file);

    try {
      const response = await fetch("/picture", {
        method: "POST",
        body: formData,
      });

      if (response.ok) {
        const result = await response.json();
        alert(result.message);
        console.log("Server response:", result);
      } else {
        const error = await response.text();
        alert("Error uploading file: " + error);
      }
    } catch (error) {
      alert("Error uploading file: " + error.message);
    }
  }

  function handleFileChange(event) {
    file = event.target.files[0];
  }
</script>

<div class="upload-container">
  <input type="file" accept="image/*" on:change={handleFileChange} />
  <button on:click={uploadFile}>Upload</button>
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
</style>
