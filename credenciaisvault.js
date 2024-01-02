npm install axios fs-extra

const axios = require('axios');
const fs = require('fs-extra');
const path = require('path');

class VaultCertificateManager {
    constructor(vaultUrl, vaultToken, secretPath, vaultFolder) {
        this.vaultUrl = vaultUrl;
        this.vaultToken = vaultToken;
        this.secretPath = secretPath;
        this.vaultFolder = path.join(__dirname, vaultFolder);
        this.certFile = path.join(this.vaultFolder, 'cert.pem');
        this.keyFile = path.join(this.vaultFolder, 'key.pem');
        this.certificate = null;
        this.privateKey = null;
    }

    async connectToVault() {
        try {
            const response = await axios.get(`${this.vaultUrl}/v1/auth/token/lookup-self`, {
                headers: { 'X-Vault-Token': this.vaultToken }
            });
            if (response.status !== 200) {
                throw new Error("Falha na autenticação com o Vault.");
            }
        } catch (error) {
            console.error(`Erro ao conectar ao Vault: ${error}`);
            throw error;
        }
    }

    async getVaultCredentials() {
        try {
            const response = await axios.get(`${this.vaultUrl}/v1/${this.secretPath}`, {
                headers: { 'X-Vault-Token': this.vaultToken }
            });
            return response.data.data;
        } catch (error) {
            console.error(`Erro ao obter credenciais do Vault: ${error}`);
            throw error;
        }
    }

    loadCertificates() {
        if (!fs.existsSync(this.certFile) || !fs.existsSync(this.keyFile)) {
            throw new Error("Arquivos de certificado não encontrados.");
        }

        try {
            this.certificate = fs.readFileSync(this.certFile, 'utf8');
            this.privateKey = fs.readFileSync(this.keyFile, 'utf8');
        } catch (error) {
            console.error(`Erro ao carregar certificados: ${error}`);
            throw error;
        }
    }

    initializeCertificates() {
        if (this.certificate === null || this.privateKey === null) {
            throw new Error("Certificados não carregados. Chame 'loadCertificates()' primeiro.");
        }

        try {
            // Aqui você pode adicionar lógica para inicializar seus certificados
            // Por exemplo, configurar variáveis de ambiente, etc.
        } catch (error) {
            console.error(`Erro ao inicializar certificados: ${error}`);
            throw error;
        }
    }
}

// Exemplo de uso
const vaultUrl = 'http://localhost:8200';
const vaultToken = 'seu-token-do-vault';
const secretPath = 'secret/myapp/database';
const vaultFolder = 'vault';

const manager = new VaultCertificateManager(vaultUrl, vaultToken, secretPath, vaultFolder);

async function main() {
    try {
        await manager.connectToVault();
        const credentials = await manager.getVaultCredentials();
        console.log("Credenciais obtidas:", credentials);
        manager.loadCertificates();
        manager.initializeCertificates();
        // A partir daqui, os certificados e credenciais estão prontos para serem usados
    } catch (error) {
        console.error(`Erro durante a operação: ${error}`);
    }
}

main();
