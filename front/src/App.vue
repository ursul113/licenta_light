<template>
    <div id="tools">
        <button id="run" @click="run">RUN</button>
        <button id="save" @click="saveToFile">SAVE</button>
        <div>
            <button id="load" @click="$refs.fileInput.click()">Load File</button>
            <input
                    type="file"
                    ref="fileInput"
                    style="display: none"
                    accept=".ps"
                    @change="loadFromFile"
            />
        </div>
    </div>
    <div>
        <label for="load_from_db">Select a code from the database: <br></label>
        <select v-model="selectedName" @change="fetchCode" id="load_from_db">
            <option disabled value="">Load saved code</option>
            <option v-for="name in codeNames" :key="name" :value="name">
                {{ name }}
            </option>
        </select>
        <button id="save" @click="saveToDB">SAVE TO DATABASE</button>
    </div>

    <div class="main-container">
        <div class="left">
            <label for="ps" style="font-size: 40px">Code</label>
      <TextArea
              id="ps"
              name="pseudocode"
              rows="30"
              v-model="inputCode"
              placeholder="Write your pseudocode here, import a .ps file, or load from the database codes you previously saved"
      />
        </div>
        <div class="right">
            <div class="input-section">
                <label for="input" style="font-size: 40px">Input</label>
                <textarea
                        id="input"
                        name="input"
                        rows="5"
                        v-model="keyboardInput"
                        placeholder="Write your keyboard input here."
                ></textarea>
            </div>
            <div class="result-section" v-if="result">
                <p style="font-size: 40px">Execution Result</p>
                <pre>{{ result }}</pre>
            </div>
        </div>
    </div>
</template>


<script setup>
import {onMounted, ref} from 'vue';
import TextArea from "@/TextArea.vue";
import {inputCode} from "@/main.js";
const keyboardInput = ref('');
const result = ref('');
const codeNames = ref([]);
const selectedName = ref('');
const backendUrl = window.location.hostname === 'localhost' ? `http://localhost:5000` : `http://${window.location.hostname}:5000`;
async function run() {
   const data = {
      pseudocode: inputCode.value,
      input: keyboardInput.value,
   };
   try {
       const response = await fetch(`${backendUrl}/process`, {
         method: 'POST',
         headers: {
            'Content-Type': 'application/json',
         },
         body: JSON.stringify(data),
      });

      if (!response.ok) {
         throw new Error(`Failed with status: ${response.status}`);
      }

      const resultData = await response.json();
      result.value = resultData.result;
   } catch (error)
   {
      console.error('Error during fetch:', error);
      result.value = 'Error: ' + error.message;
   }
}
function saveToFile() {
    const blob = new Blob([inputCode.value], { type: 'text/plain;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = 'pseudocode.ps';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
}
function loadFromFile(event) {
    const file = event.target.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = async (e) => {
        inputCode.value = e.target.result;
    };
    reader.readAsText(file);
}


onMounted(async () => {
    try {
        const response = await fetch(`${backendUrl}/load_names`);
        const data = await response.json();
        codeNames.value = data.names;
    } catch (err) {
        console.error("Failed to fetch names:", err);
    }
});

async function fetchCode() {
    if (!selectedName.value) return;
    try {
        const res = await fetch(`${backendUrl}/load/${selectedName.value}`);
        const data = await res.json();
        inputCode.value = data.code;
    } catch (err) {
        console.error("Failed to load code:", err);
    }
}

async function saveToDB() {
    const name = prompt("Enter a name for the code:");
    if (!name) return;
    try {
        const res = await fetch(`${backendUrl}/save`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ name, code: inputCode.value })
        });
        if (res.ok) {
            alert("Saved!");
            const namesRes = await fetch(`${backendUrl}/load_names`);
            const data = await namesRes.json();
            codeNames.value = data.names;
        } else {
            alert("Failed to save.");
        }
    } catch (err) {
        console.error("Error saving code:", err);
    }
}

</script>

<style scoped>
#tools, #tools div {
    display: flex;
    justify-content: center;
    margin-bottom: 20px;
}

#run {
    background-color: lime;
    color: white;
    padding: 10px 20px;
    margin:10px;
    font-size: 16px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    text-align: center;
}
#save, #load
{
    padding: 10px 20px;
    margin:10px;
    font-size: 16px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
}

#run:hover {
    background-color: green;
}

.main-container {
    display: flex;
    gap: 20px;
}

.left {
    flex: 1;
}

.right {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 20px;
    padding-left: 10px;
}

.input-section textarea {
    width: 100%;
    padding: 10px;
    font-size: 14px;
    border: 1px solid #ccc;
    border-radius: 5px;
}

.result-section pre {
    background: #f5f5f5;
    padding: 10px;
    border-radius: 5px;
    white-space: pre-wrap;
}

</style>
