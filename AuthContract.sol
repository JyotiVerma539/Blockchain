// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract AuthContract {
    struct Record {
        string cid;   // IPFS Content Identifier
        bool exists;
    }

    mapping(string => Record) private records; // UID => CID

    function storeCID(string memory uid, string memory cid) public {
        require(!records[uid].exists, "UID already exists.");
        records[uid] = Record(cid, true);
    }

    function getCID(string memory uid) public view returns (string memory) {
        require(records[uid].exists, "UID not found.");
        return records[uid].cid;
    }
}
string[] private uidList;

function storeCID(string memory uid, string memory cid) public {
    require(!records[uid].exists, "UID already exists.");
    records[uid] = Record(cid, true);
    uidList.push(uid); // Store UID
}

function getAllUIDs() public view returns (string[] memory) {
    return uidList;
}
