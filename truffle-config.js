module.exports = {
  networks: {
    development: {
      host: "127.0.0.1", // Ganache
      port: 7545,
      network_id: "5777" // Match any network ID
    },
  },
  compilers: {
    solc: {
      version: "0.8.20", // Match your installed compiler version
    }
  }
};
