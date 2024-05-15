import { app } from "../../scripts/app.js";
import { getPngMetadata, getWebpMetadata, importA1111, getLatentMetadata } from "../../scripts/pnginfo.js";
import exifr from "./exifr.js";

async function handleFile(file) {
	if (file.type === "image/png") {
		const pngInfo = await getPngMetadata(file);
		if (pngInfo) {
			if (pngInfo.workflow) {
				await this.loadGraphData(JSON.parse(pngInfo.workflow));
			} else if (pngInfo.prompt) {
				this.loadApiJson(JSON.parse(pngInfo.prompt));
			} else if (pngInfo.parameters) {
				importA1111(this.graph, pngInfo.parameters);
			}
		}
	}
	else if (file.type === "image/webp") {
		const pngInfo = await getWebpMetadata(file);
		if (pngInfo) {
			if (pngInfo.workflow) {
				this.loadGraphData(JSON.parse(pngInfo.workflow));
				return;
			} else if (pngInfo.Workflow) {
				this.loadGraphData(JSON.parse(pngInfo.Workflow));
				return; // Support loading workflows from that webp custom node.
			} else if (pngInfo.prompt) {
				this.loadApiJson(JSON.parse(pngInfo.prompt));
				return;
			}
			else if (pngInfo.Prompt) {
				this.loadApiJson(JSON.parse(pngInfo.Prompt)); // Support loading prompts from that webp custom node.
				return;
			}
		}
	}

	else if (file.type === "image/avif" || "image/jpeg" || "image/webp" || "image/jxl") {
		const parsed = await exifr.parse(file);
		const userComment = parsed[0x9286];

		const json = JSON.parse(userComment);

		if (json.workflow) {
			await this.loadGraphData(json.workflow)
		} else if (json.prompt) {
			await this.loadApiJson(json.prompt)
		}


	}


	/*
	
	
	*/
	else if (file.type === "application/json" || file.name?.endsWith(".json")) {
		const reader = new FileReader();
		reader.onload = async () => {
			const jsonContent = JSON.parse(reader.result);
			if (jsonContent?.templates) {
				this.loadTemplateData(jsonContent);
			} else if (this.isApiJson(jsonContent)) {
				this.loadApiJson(jsonContent);
			} else {
				await this.loadGraphData(jsonContent);
			}
		};
		reader.readAsText(file);
	} else if (file.name?.endsWith(".latent") || file.name?.endsWith(".safetensors")) {
		const info = await getLatentMetadata(file);
		if (info.workflow) {
			await this.loadGraphData(JSON.parse(info.workflow));
		} else if (info.prompt) {
			this.loadApiJson(JSON.parse(info.prompt));
		}
	}
}


const ext = {
	// Unique name for the extension
	name: "Example.LoggingExtension",
	async init(app) {
		// Any initial setup to run as soon as the page loads
		app.handleFile = function (file) {
			handleFile.bind(this)(file);
		}
	}
};

app.registerExtension(ext);
