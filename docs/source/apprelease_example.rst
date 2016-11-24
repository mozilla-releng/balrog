.. _appreleaseExample:

========
Firefox-43.0.2-build1 blob
========

.. code-block:: json

    {
        "schema_version": 4,
        "name": "Firefox-43.0.2-build1",
        "appVersion": "43.0.2",
        "detailsUrl": "https://www.mozilla.org/%LOCALE%/firefox/43.0.2/releasenotes/",
        "displayVersion": "43.0.2",
        "fileUrls": {
            "*": {
                "completes": {
                    "*": "http://download.mozilla.org/?product=firefox-43.0.2-complete&os=%OS_BOUNCER%&lang=%LOCALE%"
                },
                "partials": {
                    "Firefox-40.0.3-build1": "http://download.mozilla.org/?product=firefox-43.0.2-partial-40.0.3&os=%OS_BOUNCER%&lang=%LOCALE%",
                    "Firefox-41.0.2-build2": "http://download.mozilla.org/?product=firefox-43.0.2-partial-41.0.2&os=%OS_BOUNCER%&lang=%LOCALE%",
                    "Firefox-42.0-build2": "http://download.mozilla.org/?product=firefox-43.0.2-partial-42.0&os=%OS_BOUNCER%&lang=%LOCALE%",
                    "Firefox-43.0.1-build1": "http://download.mozilla.org/?product=firefox-43.0.2-partial-43.0.1&os=%OS_BOUNCER%&lang=%LOCALE%"
                }
            },
            "release-localtest": {
                "completes": {
                    "*": "http://archive.mozilla.org/pub/firefox/candidates/43.0.2-candidates/build1/update/%OS_FTP%/%LOCALE%/firefox-43.0.2.complete.mar"
                },
                "partials": {
                    "Firefox-40.0.3-build1": "http://archive.mozilla.org/pub/firefox/candidates/43.0.2-candidates/build1/update/%OS_FTP%/%LOCALE%/firefox-40.0.3-43.0.2.partial.mar",
                    "Firefox-41.0.2-build2": "http://archive.mozilla.org/pub/firefox/candidates/43.0.2-candidates/build1/update/%OS_FTP%/%LOCALE%/firefox-41.0.2-43.0.2.partial.mar",
                    "Firefox-42.0-build2": "http://archive.mozilla.org/pub/firefox/candidates/43.0.2-candidates/build1/update/%OS_FTP%/%LOCALE%/firefox-42.0-43.0.2.partial.mar",
                    "Firefox-43.0.1-build1": "http://archive.mozilla.org/pub/firefox/candidates/43.0.2-candidates/build1/update/%OS_FTP%/%LOCALE%/firefox-43.0.1-43.0.2.partial.mar"
                }
            }
        },
        "hashFunction": "sha99999999999999999999999",
        "platformVersion": "43.0.2",
        "platforms": {
            "Darwin_x86-gcc3": {
                "alias": "Darwin_x86_64-gcc3-u-i386-x86_64"
            },
            "Darwin_x86-gcc3-u-i386-x86_64": {
                "alias": "Darwin_x86_64-gcc3-u-i386-x86_64"
            },
            "Darwin_x86_64-gcc3": {
                "alias": "Darwin_x86_64-gcc3-u-i386-x86_64"
            },
            "Darwin_x86_64-gcc3-u-i386-x86_64": {
                "OS_BOUNCER": "osx",
                "OS_FTP": "mac",
                "locales": {
                    "ach": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 80088440,
                                "from": "*",
                                "hashValue": "c3f7de52a18bbbb1238a83d5e9a342810b18a75d76024a7dc0cdb099154c8fec679c6ff6bd7041b14983688527d2402ebe69ddd6b328354f5c10e96662639b66"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 26957345,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "48e842ad26eb72d1726aa94c2e22d0a08e65ac1cbc6b8265885a5c37a0eff47d997da23f9e5d02862897de5e58d00a4e8460a283dc4bb113a0f4e10266e22d5c"
                            },
                            {
                                "filesize": 44169271,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "fbbebed48152bf9e1aaf95c0f703432bc9234d0d454f6d3aef063293efb89287a783a54b0b63d083c73c855545bb6dc42f8e7dc9e0c2843367e6ff83605b411e"
                            },
                            {
                                "filesize": 39597136,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "1440d36670d27af395a8d261b93d8157b1a8ba363fbb098b7849e9f949e59b9eef67494cd705b24f32d3bce7c46553871494fbf50ff894498a0bc5ae217955a7"
                            },
                            {
                                "filesize": 134857,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "3a11a788af0b8387b2c3992443e4cfd050ca3970baa98057468823fe28237c3a789835748acbcdea7f9b439b75961c14bf7ca86a6aecd43d983be63102b8c583"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "af": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 80094667,
                                "from": "*",
                                "hashValue": "4ba61f1a12a1ecbcf2ae348e96ebcb2a9b04a06113761bcbb6ab5fef03828e2cd65cd08890c16f7a4a53f022b20b5a6262aed245abc0746fc358fa28e2a40e75"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 26908671,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "40a307c527299585b5023447ecf362b7bdc356d9f6237b340f4b8a80dc0bc21016b16ebe972f39533b2a93dd50a9e6f5dc845c82fd363f5384c7997416d2c8bf"
                            },
                            {
                                "filesize": 134500,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "a927f8d21129f2c835a61d51183be6a5b58a2dca5f97ad4ae1fb3da6d81e0ee54e436c4e70324571708b752442928f065771c42d44e952b7345ce85247790bce"
                            },
                            {
                                "filesize": 44141629,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "ceff60a4604ca61f8fe68c398f3fe9d5c0c75aa5c1073fcbb5d76e05572b09226a751bb9aa75826b0d0400b9d995dba55cf07a83564d5d7c7c9a6b0f0154c192"
                            },
                            {
                                "filesize": 39533952,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "44a44651072b293d0436ac624bf4da0f4e2a9fa96862ca76e63f0b60baf53b0b5b8017edb8ed8b206ebe4804a83e23930e82c79f2cc0402cce2801643e544ff4"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "an": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 80073120,
                                "from": "*",
                                "hashValue": "a503df5f989c7d84e6947349231f7020fcc6f9af35f77dd54ea6c28826679e40be9aee2ad34bc0f21e170a9e5d84ff5b49a11550d7286d47ca4a40d836d9812b"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 44100184,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "916fab326166927c3a53a3db8fcb495050310ca8efa09709da53fb9430c68155d68cee3251ea0115b8cbbccd3b3cf9afddd0a6bec3680c2c7f4b83b0ffdce157"
                            },
                            {
                                "filesize": 39509177,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "6bbe9b1798cfc176869fc6d51da4c59f4da5b0498efbc9987133d88375acafcfd25020dd2d0a467b348382985b7be39b280544a0c22f84182b12611643f35188"
                            },
                            {
                                "filesize": 136435,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "0083b09a3df1110fabca7e51cfa3bc58a39db72254cfbc97159c36d341141d3b6c47b167f7d04451f76f512847cc00c61174457315f95b7bb9177ebf7de6bacf"
                            },
                            {
                                "filesize": 26907626,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "136504092062bcf8e34945f0b9190430448a49ccf7025b4fd157f3f16b869dd3138ae7d708d47c83d44483413202c7b573c11a05b93278f407d0601d6f41b017"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "ar": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 80134146,
                                "from": "*",
                                "hashValue": "77d0a4b25844df74e96f4661986b4d103e00d1317ba3d7267ed46debce96c2bb52c25f495a3efe093dbf60a7267f5ba1f0361935b78ca6311618949aabad2502"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 44173565,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "170bfac59355be276300a3462927aea6e60e2600a0f8a12bbe708109127d95d6dca23ea2311df56cf0688162e369d3d595eb10f916fc8c788b0e46c0950018f8"
                            },
                            {
                                "filesize": 26897790,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "ed68348ce670da32fe1b666bb072cf41c5adae77feefb9dd24b2c8617015484bb07d7d05fc0149ea34377d9be7012ec3344de871e7e3c5fae9f3d157a3acb26e"
                            },
                            {
                                "filesize": 134617,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "8dd80676bc0912c1a103b4f769e46109d67622dea13e38dc042992e085384d0f42a45ec333d1df1cdb7046edddd8e17734439875c8c282223fc5f2dda3f75959"
                            },
                            {
                                "filesize": 39563731,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "e6f746d54849a62147cfb5fd516cf004ba0a483a1c4c4b68a03f871b96add364bf11b216f58e00bdf03bc6d50732edef31305f30d9da5150ac96ee83fb97249c"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "as": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 80121557,
                                "from": "*",
                                "hashValue": "fbe4041400d0b30ce33e7f22a143e6a04e5d95bb5e64e7e9ce8978d4fe0a2c19f7d55da456ed403509e657bfd45d0dbcac333849cb23620e2266ad379dad18a2"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 44114121,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "cf90d1acfcbc19149bc203d4693794cfe44935f2abfd0b7a0c87beb26a64ad99c94db307d28acee11256f70e1e8025bc15a3e78f7c46c8a1e4061f7bfc99d493"
                            },
                            {
                                "filesize": 135477,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "14414a7e86b3e12a6b8a5d7d1fed52477c6aa9760a492c4de1b3f326d803c16ce1de0f5691ec7b3185038498240fd6c30ff4d59fcaebccb9f202f504b69a938e"
                            },
                            {
                                "filesize": 39519057,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "db086338cefbd47cb9f7cb77cf06f9540bc9490cf3bd75faa9d84cbc4de31a47528249440efcd7e5be53d1921d4429f782ed091c05796cf001a7befb4fa2dddb"
                            },
                            {
                                "filesize": 26910848,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "7dbef454482deb01ebeb35a43605ba730fcc4a5779a8ca783723205a4261f12ecb9df379df3cff029bd81a81b1f8c586ff980d3a49a1942ea2af9712910e2c4d"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "ast": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 80013878,
                                "from": "*",
                                "hashValue": "edd4148c7630ef4017ac29304844df490e7d917614f524ca43203bb2a3d052853a05a1ddd3232b4566b634b89a772315b0caef86369fa37cb1072cc9228a3087"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 39465080,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "8cef8e5afac7c1b7f9d0ea8f258c9a6491257f454e5ff4a296541cfc7bffc626c6ba0638aaaa1060837bd99330429376ba74802845a51360ed0fe04600b7d459"
                            },
                            {
                                "filesize": 135850,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "537a3249412b190c29324df450f01649a53f5062f9d68151116c915470cfec7883c32ad77571e70ad07ccf6139640c3c6a7a3a5b4efde6df6f89b826fa622ddf"
                            },
                            {
                                "filesize": 26883485,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "7b2fc6d2a9f83a0dde7692da8f7fbf9d14cf8c8ffe2eee0b7f67cd80c718ab0c1925b7a6f8072c711812d1d571694959d5fcedc917f3207afe6e3006903b7c15"
                            },
                            {
                                "filesize": 44049826,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "a1441465a35e30b7b5339219362b2e6068309447f45bf8726784b8e84ea60b9efda34a38a4af72048a0aff869de26204973709a01b14c31dbe1e06ce689d3e75"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "az": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 80102593,
                                "from": "*",
                                "hashValue": "5058f88d20ce9d3f076cd30ef87d5c08884a5ad796e1e713291f13ef04b26559b0c2e329e8dcb6424648b39bffea8dee449f4b6a7c5196cb819e763a47d171e7"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 133701,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "a6eef9a5a45ec154fc588f19ca4393586c784f6a7afdde6cc6f2e1193cc870f83a5cdd6aad5553b57e411c525d17d5b01b7d9e301516abea3c2b721567802ef1"
                            },
                            {
                                "filesize": 39564208,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "726401b1906cae0ecf0a8034b621afccce463740df66f1758b51805cfa79edc0b5ce747b5d9291517e1904b7f7c7f16a6bab4abbbd002240b904f0abc969c3c4"
                            },
                            {
                                "filesize": 26955542,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "92991d1cf78eec9bf550bf5d2c374930c3d83ea02903950de10c475111d17ddc8ee593354486333c26a0a05e80319402abf60d94b572ed7a25aebccf4c3d7417"
                            },
                            {
                                "filesize": 44171347,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "eb187763a1888450886bc471a6057b860bf96f5d62568b691de9bbec62c3f755a6765db211416f30d4d9fe61224a0cc7195520b6562defcf8ad77b1633100cae"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "be": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 80064542,
                                "from": "*",
                                "hashValue": "b874aaa321d8527f97d74cd842e971bbaecba56de2b59f465fd74030515856601da73aecc4284109b7c16a5d0cb37afc0596d0f90cf4b5d5c32d8370438a9cee"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 26895654,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "eec91739f4ca44dcbf45810f159a7ae4fa3b427bc5c76e458e6c913fe7e0a579751a9a69e2347ce90b9305a5026e180337ff15b267953252267b96c71942313b"
                            },
                            {
                                "filesize": 44088976,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "0f8c71c7e43b0e1292225a011ac6c4cc5f5969ef2319d1a15e6d368cf132aec77bb691e1c1f6d943b15d6f811f3fec138021d49f6a5ef104940d2297b96c7a30"
                            },
                            {
                                "filesize": 39492418,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "997352af1cdc030b8c9ad727f067cb2fce63327a0ec146ec0dd2cde175648da0028d6416208f3235a60fc79bb686ab81d4d64c60f6b919f7506b6794a52d97b0"
                            },
                            {
                                "filesize": 131867,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "7a16989c8320405468d98b25a7149025d88302060cc57c2b0fd3bb986b7752b034730d91274e6e8b6646b358a0b6cb655771729ae4404549ba7df649c9a280de"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "bg": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 80373174,
                                "from": "*",
                                "hashValue": "98bec63605430d92db467513c27bc06256389059152d2fbd59ee2c6393f1c356869627c926fbd6e4fb4ed9e23ed05552a093e78dfff9b9fc31a2412d395414c4"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 132621,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "37fb0668d7aa4befbc32fc5c4198cf38d0dfc55166de5372a91d6717adb3c971469a8145c2edc3271e236c918fac839c821042bb6a852260420b3d18956b6c33"
                            },
                            {
                                "filesize": 44218009,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "db5b76794b8037b4fcf723441201fc86babf92c11f11979a79c8d18dc0520f5bdb73cd66f1725ca5bf2d94924a18256c9a748a5d74b957f34d948051486754ab"
                            },
                            {
                                "filesize": 26977714,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "0f952466b1cdc1448923d0c1c5a27852c8f90afab0220da2befb88933c1df8ecf958a5c6a6028421b03529dafbf9b7c65fad9f408aa18b79b5204bb2f1d35665"
                            },
                            {
                                "filesize": 39648831,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "ad3efe8c448c33a4c1d29acc5c961e221428f62cd62d7b004420ce23c7d7827eb5a01321db9b049ea8b3b73e65af5344ffc3f3dfed40e56e89ac044c9f6c1775"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "bn-BD": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 80148536,
                                "from": "*",
                                "hashValue": "b2eb155783a93d1ab193fd3504a0f18a95c7f2dbebbff1fd6ff592d1adffe5ff6a04f460cba1a80f368804304e5130c6963463202d3ef63bd875b9aebcfefc05"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 134031,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "dd54b86f191ce4ee07c98db0e3b96d74964a99ee14ef42803b18da3e9c5e63b9d4cfa60438ad636c4161de1cb2dbafa5e462a8ff108f06373ef4589a2a2ab207"
                            },
                            {
                                "filesize": 39738524,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "0ada55ac8b1e17c97d1bab069298038a0639bff8110139ef4cb45e389a8f7f1cbec6066797df0ac63de8fcb6e3973c5a6f42e610d2c9fa52dd9996fa412109a4"
                            },
                            {
                                "filesize": 44307840,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "aab26745015aaa88be7509961f68e2e5f8ff607f779ad9e8f751d8b3b681a570fff4d85efbe8bd3f729572a6aec12e996bfa80df46a45bd682c5f4c0cddcbf8d"
                            },
                            {
                                "filesize": 26908345,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "1b7534e909a05bd210435318bdd5142ac95d7e67a7b3cf2389575819c6f74ad283a4a0ee11d224c505e7d04a0d67f4472840f6c14c3ef2ab8155db9748fac930"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "bn-IN": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 80140601,
                                "from": "*",
                                "hashValue": "78c4108e29a2e1de081c6032abf53c2b641db02a89ff0c3d5c325be841f47a78ac0e391fe360003f0ac543bfb1a0a5bff3dd3d0eb9ffc72062394dcf1cff11be"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 39667142,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "164c7320e347f5385c84ba5d2f6439c2db28a51339953f85b1ca6e612a28b39d62ce0fa9aca3628aa91173dcb4db3137b69e7892cb774fc1bb7a86b5dec763af"
                            },
                            {
                                "filesize": 132572,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "3b956bc08bc6053b5a4f5f3a35152f0e8df2ce36f1ba43a6fb58271f98300c815a877604e5796d68b0a006d0d092d899fb60186f50d6f5e86939fdfd77432fbc"
                            },
                            {
                                "filesize": 44232505,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "53788c25f265f843da4ca4bfe8ab3be955378290e39afa91df3d6b4bf51d7d90eb3eed70266fc14f04f557683a0f3e892a3c35c90fcde0b6888d0a29690ecc10"
                            },
                            {
                                "filesize": 26909941,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "0849266bc69fc709f8a54decb529d07321c34a3f5b3e935b401e4cad786ba168aa943f1ef2d6d5dc670f66306b286ab453f02cd2519ed9d2ed8c01410b945e7f"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "br": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 81418837,
                                "from": "*",
                                "hashValue": "8906e6444020b6542f22a3ee31154d57af78ce6a87ba23f1bb51618e905eec338252ab2c0d9dadd287f8db19b65f2baf47dd6d39e310863ee38fab27e7774a75"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 39514273,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "0eff15efd4625683414afbcc3fccf4565e84aea08b493048618c3fd996863b63ffe159f4df08083ef5833004e1cacfbb75a861256546c372bdb25d52ed4d6399"
                            },
                            {
                                "filesize": 26894915,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "eec5c75bab29c95dcf9307e2c089849b9b9891c183202ae69a99c565d28ad39444b079d03573c071a25a43bc9032dc24e1d9217d10bfcab3841d907f2f7934e9"
                            },
                            {
                                "filesize": 44098411,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "47c5e64b212ffa94b5313a5fdae8f8c000c25573776f033ce77c82ec3ccb90d635d9820b1c26b0872301bd206b28d7dbed0c3b21dca3c7848bf3449c309643a1"
                            },
                            {
                                "filesize": 139152,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "9b4a16c04a9e0037caede4a1e8ffc2e65e24b8dacc5b62db9bad054e0f1b41d36ec08a5431dd1945980a48e131b73fa62a0c7fed580f27da4f97b593782b3de5"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "bs": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 80093525,
                                "from": "*",
                                "hashValue": "b64c56df29d682b1aad09428e4fef3001966ad58bacaf4fa837ad16f298d24cb4759a70fd866e6b6cfc8efd32b0199e84d66afb88ff5e246e0987292ca402b61"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 26907382,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "c68e9a5f248085b910a1f68d7a3d0633a8201c2e8525df427d665001ccc6b0d84358194a498f4ef4904611979dc09abf7c648ffbd5168a6fa1a4a4e2e4934a1f"
                            },
                            {
                                "filesize": 44275500,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "6ddcd241b6cc6a24123525a995d18d8218dd51d6ed400e55fceb43bccee498a4c37cbfd5a48f07b2ba50ed3534fd80148cf9190291e62726b732fd8c14f0bdf5"
                            },
                            {
                                "filesize": 133876,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "dac64003aead90fb20dad87414f2d03e41b4cf851ff46cd40ad66f3dbda5e03d6441854b9e6b7362960c0efb94c31a093ad01da2b7a0a19e6a940b051fbaf8d8"
                            },
                            {
                                "filesize": 39530416,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "4a92c9e0bab2f77e2fa1fe96ef268d4aee1c408d91209a3009ecec9b6ca9e4b37e48f09022b3c0cacfae18c2a5bb0ffdf88a11d798956622b3f7cd16402e2c2e"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "ca": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 80475569,
                                "from": "*",
                                "hashValue": "13514928333b25448e9ec53575a84c76aedf30b9ff017a0fa20d5b094dc223214603ad581676e6d4a38a5bf02476dda9f63ea5b683013c73bff85ca3bb76e0a0"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 134755,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "5c1fd931151257c51a204cf330e1d1021ac96801c1203091a61b24ef58c2ee2f2ede549124de61c45b289feecd657b1e482a5ca6e318cac60d89f08220fc4e16"
                            },
                            {
                                "filesize": 39550696,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "144f8a1b7309fe55ebc56b2bddc6acb5b8e64f3fcdd02c01fc86091eb72e72a8f17ece849e4d4651962f6682fdd317e073127962a7e7e53d74254312972882b5"
                            },
                            {
                                "filesize": 26933179,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "c3b1bfb3d7d3e5d9439d09541c3c2d62330487c76d90a6c1645e6713b55634cd313ad7db73881fb5cdb081e85efdec4fdb255acf31c0c3ad75bb19a6ea3917ad"
                            },
                            {
                                "filesize": 44140125,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "cbda953ad8115e9c51b351e83596b00096017252b8ced9b229f8de7e2356dd1d7de5d9afd9dd33a4168b893ad42e544c3e0c54696c9d6d9660fc4455d3dc282a"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "cs": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 80059271,
                                "from": "*",
                                "hashValue": "24edf061cb0e1b8f6a35ae1d0ddce586a10ecb77ab678de5b91b34d7ae43bfda89e13a7a1a14361dc59ef8abddc8fe119a50056a4e614d6015fa7e51b522d288"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 44145303,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "0108b4a694f5083cec6a244fc1342ae94cd5e78e35a697add5af59241af40bc7dae7939819b8e27fe4515235ff1b340c2a23fe58c47211d0237731b65c9656ff"
                            },
                            {
                                "filesize": 39530230,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "3718665aa6f3e1c74d8192c416b77406486ee05bc3229475d166c23f6c8751ed1788ba2e328b2701cddd99be4a482c86d6a7b16b8b6427e5b5cca3622f367924"
                            },
                            {
                                "filesize": 26917303,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "51563a4a87000b3147eba120d36e4c2744a73b6ac6db487678948195300c0c0196685411a1491ca0e39c257368db0c67b4836ffcf8a34dfa0151e6e4284369e9"
                            },
                            {
                                "filesize": 135684,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "eac415696aa5024f3886a354bba7c384ffd0ad391e8b24f236a346236a4125cce8f72e38e724ae45a4757ec4a6797bb8a1845dddade238d1f6a9160de1077697"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "cy": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 80052797,
                                "from": "*",
                                "hashValue": "e5a3dba266186d2006b2e4ff6734076931fdac068792463e48c3029a8ece537ec56bb91bd01eac18655f78ac3bbd4a721c66fec6fb238538a034d8e937ae0bfc"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 26905187,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "17e88ce8b1d8cca2dd28a80dabd5c9a9bfc6d5adeec26345620046506f26056624249de030fe733f19f38cec48cb43b63ec422c1c5d7ad3096d28c3a941f5241"
                            },
                            {
                                "filesize": 39503135,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "45eb4095a1ecdb4e850cd5a1435edc429b506dbc9e80273fc5a75d5c1daaeae31429b02d8c01d4161d91725bd6f88bc17e949fdf72977b336a9955f845be06fb"
                            },
                            {
                                "filesize": 44102793,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "7b31c8c89f68de10e8ac4c9ccf1413a5aab6765277bfec7d4a74a461bbed7779459b14e4136eb84e80e6e518457d25f3dbeac48d3ac05979453c3c2a83ecbcd2"
                            },
                            {
                                "filesize": 132856,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "7949e5b27eac7d4f1235e73ba4b7c86d3c993a2530fab6e443f98b320f754d5b92a47eccd2108fcbaa61be64425ce93191d71231449ac65be24a15593282f0d7"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "da": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 80687253,
                                "from": "*",
                                "hashValue": "da0d1d57d679301badbd523e88026e2aab3c3d24364d60dee12ade39d4c38490d1ec9592ba4bdc207e2f7065b600c6964e3c70fd349dc46d3f3ba7da38231ae6"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 44101050,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "32bd2013ed581efc0363658577a28448df064a0177ff786d1a3dd61849e84ce7731c027278ef144b7b05e433adc4791585723698cd166de4ecc89fd34cf2c785"
                            },
                            {
                                "filesize": 26896828,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "d19c4d2428698cb9e9cdf90fc72ae0720d3da090fc21f4aff981b2f499cc1cb056e4695b037c5852a9bdd09b7aabc9d46c9322479a0a504f7ca65af7c1f9a36e"
                            },
                            {
                                "filesize": 136853,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "7ae5b7c3b48511924d9f17c4386d6bfa00271efdac225de0b2dd1472856bf71fcd9c88dc09b1179ee28b7ee91da59a05702b0b1cc4567d4bbcfc0a482e8bb8d2"
                            },
                            {
                                "filesize": 39496290,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "8db6b373be98c9cef3a1e25687168132bc8e079799ff3add4b73704510aef06c2be0b1c42dc9585f0ac88d18347bb8759fe8d9488722441c4db42fb9968930a3"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "de": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 80065717,
                                "from": "*",
                                "hashValue": "0586240c99424635b3258293a959db6daa033046f4f4c705c3b3e710d78606b24f8f77578a4f645534158140bf1b9ec1d43af89a18684fd09d4ce4785e81bfd9"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 39510844,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "dad265747542b98901cb333fa4a28d4c863ac5ddc3765b40221938cc4a5fe3acbee0f3abe9c4d64ccbd59196e8a4062fc665a51ff176e68b7a60b81cb493e241"
                            },
                            {
                                "filesize": 26906280,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "8fb038a26e2cc7e664679dcb1d6c10a87a2200657728a5d81fc90df9394b6e2c3eee78da41a25b3e69dda1fafbe8c69e51a03be0723fb1aa0af3c79f1eac7d86"
                            },
                            {
                                "filesize": 44105601,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "dca42bc1a45180c000d6f2b849ed2878afb8f475845e47ef21ab07ddf1870ea9df8ebae137d300da2e960d383c41c96ee641e71bd2811d0b8b790febab503601"
                            },
                            {
                                "filesize": 138596,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "36f2d963e9d8e5064e872da1da4cbea313eb9ce474d4d328bc3871fc557eff4b7b78ed84c7e62d5d0612ebd372f777aa2730eca69f8d00a40f4efa48bda9e631"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "dsb": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 80082705,
                                "from": "*",
                                "hashValue": "fcff0fbbb3987cf26940776ed5c45432bc6c71649ccadda853c37396cfeb6b68b8c50a634ea9f60a36eca1cee602bad72eb8ce516c24d6c55a12db4ebbec44d8"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 136699,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "c76fbfb2c2612f60d6bdc5d188218bacb2de382f1b3961ff9aed66051122df4ff36fb31f8ed938140d9ce0a4477f399dd3402b822e70c7ac3a6bb8bffe7cb622"
                            },
                            {
                                "filesize": 26912001,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "254e031595d2659e78d9138b634de59a15cef067d3854ba2bcff4060ef3d7a914a779b3763e7160ca1870ab97aec73201db5474a4808df75f736bbe11274138a"
                            },
                            {
                                "filesize": 39520177,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "376846b3fb222a91c0ba18a030a35a03755d0c7c2dcb63078cc95f86ed68ebaa6276152468d3f30329c9c4d366918c0a9c1ad2b02a3fd68eb75df3f441248dc4"
                            },
                            {
                                "filesize": 44113378,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "9413dc1331eae0b1060f66031d1af92b752b647a933521f2de9f688b01c04ec90effc1aaadf39c4594a3d036d9cbae9d12d466a58c4570c8339958eefb390a6c"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "el": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 80106335,
                                "from": "*",
                                "hashValue": "3da2f38ad918f5013c92f400bee67e5267ec22ce23ddfe2ae8f9f2c94787a77f015ed9ffeca0d9dad51abf359a74545d9b7542d69b527c2a6b77c69a41dc1f79"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 132762,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "a5c49d57c15762921e7a18fe80bd7f9a81fcb00d2b96e15cb27e07e4726ff8fdbc1335e2d731b072b14459e2d924c37ad9267030d07823f1444a431404d77665"
                            },
                            {
                                "filesize": 26902452,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "742b05dfa7dbc1cc70c70784cd1b415def8b96aabb3e2b0c1cefdcae1763bdb06c921a977fb03eb865bf8027572ee9308e11229b84035f49fa393b1711882acf"
                            },
                            {
                                "filesize": 39505926,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "e4c4e7b27020587c8d070dde3f17add9ec03b5def406f6569d6ae37dd781d056a6ca7d68a4111c8cb70933ca10e3e200c2fa357581dab700e1522f308adf977e"
                            },
                            {
                                "filesize": 44109669,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "e4322caab3ef651d1d8bcda866697a805bd6ee9ff02c618c2be0c7ce05b88e779a305e1278035061fc06b3084926005923fd6bcb59a0d0b54a36bfebf41cc8ed"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "en-GB": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 80045866,
                                "from": "*",
                                "hashValue": "308eeb31caab4715826887152aad211f24ce9311e22aa7475f4e33ea3d3230c7b6f22902ffac06153cbb911ecff327c9375d67a718bf486244b55c3fd99655e2"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 26887880,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "56f2f8b3121b2435dc752b01ae200deba892462951944e6245287dfb3152c1c3af056ea01490b2f728e32a11107eed7b950b2e2333d71bcb9291abd349007351"
                            },
                            {
                                "filesize": 44081098,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "585c66ff3628a8a73e8ff4ec65b53d8a2ce06aea87de5a23d9d9e78f4267d10ffaf8eb0133abea81649f8e7b2020f1175e16bfdcdd3ed1b6852bedb9079e6b00"
                            },
                            {
                                "filesize": 136465,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "96b626babf8360eeeaedd2bef0e77ab84f29939f8a1d0c21ed8e3c329f4b7843745f73a5fc35580a876ac900ffe0bdf9ec38f8e7f8089cd90bb3cb6d09f63931"
                            },
                            {
                                "filesize": 39514433,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "32dfce0983cd2556ada9116d97fc8f4c900a4d1fc2995075802cc1086093d08dfc6cdcfd66aeb7c60b55f50c9ddf3a147777133dc921d99ec91be355175c1547"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "en-US": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": "80329415",
                                "from": "*",
                                "hashValue": "781478556846b719ebc906a8a9613a421e24449b4456c4ccee990e878b3be9fb0478a78821a499a4c1f1a76d75078acf3fdfa3d0be69d2f6c94e3b6340fc935b"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": "138485",
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "895e4c9b6b108e70bea1c6d8cbe53c0cb0ada96575b0d45963544496e69cb130d021669b9e7f9a737975a4f61f36ee34249af1dcbcaa4ef9d54c61fa0a985884"
                            },
                            {
                                "filesize": "39520883",
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "6edd0803e36a03117e12a36e9fc8941e8f6321071fb00c7e8489f67b332d1cbfa95d00218e5c1b61115752fc0aecde8b2535424c521d45530455a4c5d571f889"
                            },
                            {
                                "filesize": "26917799",
                                "from": "Firefox-42.0-build2",
                                "hashValue": "68bf450a8369f6f702707e4afad1ade57b47db45cf761f29278be7f8bc682c27f512193ec22b8be3cf24ea77fc1b62727193562bdbe21bff57028913d8ba6b85"
                            },
                            {
                                "filesize": "44117982",
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "1bef3c0fa7946f7536eabd1eb00f0785575a73d3eaa6f7952a5da987e96ccaa0ec54bc86c86b675d0a1d024f6408d87743d06e631a96124f6e7bbe2f0d4e3b1d"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "en-ZA": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 80047810,
                                "from": "*",
                                "hashValue": "5a1b210d20e3d35cfd375a3e504a5ff53e1eaabcfc039c50d3e77e463b6398779ca6af4216d6e2983ceb97f0ff44c79f7629fa2c9e9b09769e280aeb5ea624a5"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 44080626,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "893f77c035e32e80b87edc784a1a017c0948fd39a5ed4f2f7caec3bdcb2e0ebbe5f62e6e5e0fe7dc0fc36513f385d60a61fd7c5d4389d215197e7f9367738d5f"
                            },
                            {
                                "filesize": 26895756,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "c4769cef2ca59d177ccfd0fda91b8289c9c1311f004a4d6f26f456187a7930de9e34efbe579dca764b2402d9f4522b96bbede92c70948381e7eb7478ce2db262"
                            },
                            {
                                "filesize": 39495073,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "58d8854d548bb9bc4f676cf152c427f989a0fe9e659d82b31735792a0ecdbe11553f9ded5011bda88e8131995e9270be05918a5497e2eff386cd0b75581a799c"
                            },
                            {
                                "filesize": 134152,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "216b2d6886add2a66b8af7521d14a85ee8b1f229fe6b94ee1f9b79df68367262e6abea187d412e1dc86ac4681693501b31bcbadf8a631b6c53907740b1af8b40"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "eo": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 80097785,
                                "from": "*",
                                "hashValue": "bcd6329c07a722d0611e1cdb2a1c81cac0e33576f9a0ed9cf3734376e8883ee73a6bba0d2f89f4895bb745957b632973afa773c6058f9cccc5f7d5716c557dfd"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 39522954,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "f0e97b808196ccaae80b813eb6265e3a4d1ab723862a2c7c0be1157351c450cb19f501c7bf4adfb236bafd5fae2a098eb1161ea685638e427e6ad12ccd779324"
                            },
                            {
                                "filesize": 44124162,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "74e140ad078f69ef4d70da64c043f237b3c57d276655fe26d2f1f6a360b737f6cddaa4c782cddb441f2b6fb9146fb0fa98a898b5167959533d511444bffae19c"
                            },
                            {
                                "filesize": 26911712,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "467a2e61a1093d6b17acd2c2dc5a684e4fa47c5b6742098ea3332218c06e8196a9c9e7965f11f9a9cfdfbbf7bbef306456d7427f9c66746274c1e81dd3aba43c"
                            },
                            {
                                "filesize": 132050,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "5cd3e6bc5919cdd0da10994a2651469dfab9be46dc56cd32e3101360ea825f24bf54aa3abdceb5bf286faa863bfcf069e4934304f19b0171dafbde34c6b4955e"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "es-AR": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 80063295,
                                "from": "*",
                                "hashValue": "73397ab2d3464df678953c7c7baa32cfb9b4c7210cf63da605e2c1396f0c1716a2359eb6f43754b3c084311d38343dfc0ea43cdb906197d4042eab4419604756"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 44103429,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "61424c30625ed6e8cafd564dd236f68be70688a63eb354eeae4743cbf40406ad7520c885099d10d044c0a1050ef3a86957ab20d5705c5b573d9a53ffe2b840d7"
                            },
                            {
                                "filesize": 135576,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "5eb0f42588a62f5527d89a7b14ca3a4cdda960afc3887770911676dbe805d08851b75a7aab8dc48a93526161f01de0ab965df89454ce73afc8315c3d48e6167e"
                            },
                            {
                                "filesize": 39508469,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "d087d4b3f3b185a6a3007d94d611fea1805794fd2b05c4db72a24853f9636808fef5808921c3d6db2f34401cdff4a98859d4771f7b5971e77f35f31c108858e7"
                            },
                            {
                                "filesize": 26903427,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "89bc6184e239f22855797d555e439d108ce73bd09291f2f797bc5a8f83217b097d822abd0160036f29bee62a469eddb52f376add3ac54dac78ed1e6ccaca9f02"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "es-CL": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 79983681,
                                "from": "*",
                                "hashValue": "c6cb7b7a6e87b42b1294e7a9827a9094cadf59be2f568a467ce1e47e5d527fae55320b96f7018b3663f6cba835689f9e4fdc5392d8f85d1fae5d525ff677b006"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 44058067,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "f8dc2335008ea346b987d6aebee86adeb1c3e869b8337f2fee283b6fc73bfeae42d59ea81e6119e3bc4da61b32ce9bf2774518a95c50a120cf06383b09a41f42"
                            },
                            {
                                "filesize": 26869286,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "f3011c99d0e9a6eb03c798b42d28679074c5163e75f55b14defb2d4c2fbec42e21da448397d4332611e4295dc8a90334e626a3fe954b169f1735ce3564753951"
                            },
                            {
                                "filesize": 39477102,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "b91be999ed33732fb29f1c6e514b56766a7610f98339de94c2dce0b1c638c0856976a59d51dd3a6706f7895a3e3214d426580d451faefb97929002086e7a8ebe"
                            },
                            {
                                "filesize": 136490,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "c51d5f367f8ea00cf313c2009ca320fc1cd799e1833628e118fc40ef1f5fbe8792281c32526fd587b2b1775ef0ae7f4806d6d47e258163ef2e43c451c554e047"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "es-ES": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 79972732,
                                "from": "*",
                                "hashValue": "e78243622770975849a953a5b0027158f5876380cf604412848192e10893738f391cbf0a5e807397e54f3aadd60b8f044d8d90b5a723dd5c0abd1ae2a0b9ce6c"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 44045881,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "c159cf9a28603fec515cee385f06610162dcf510fe609befc6ef1a001cde3fd4d3a91ab6dbdeb2f0ec6666840c4ef35828c4f834e7607b0662ec7c583183457e"
                            },
                            {
                                "filesize": 26862244,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "369a198bc93cfed4627a02488304adb067bc3224ed6ee6942ab1074766a85248c6a4a16190b7642c9934b426e52a67f7a9c6c704f28ac1aeace7525c7a657cc4"
                            },
                            {
                                "filesize": 39462819,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "9a4437af99e5bb2c1d768cbb98a255f0ad7c11979de6432d71e65e37fe2ff63b568f83aafb9d07d2c57eda28754c19a7150e00d6c6a32d3c2ab56e97ad65b9a9"
                            },
                            {
                                "filesize": 136017,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "1ebead1d720e5429ed6cacdd9270bdf7d05dac47bec509e3dea364f7849773408f4c21f67494bd7f091ecde4f100076f11b7f1f8ae09e75d08ec9a48ac76cefb"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "es-MX": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 80068576,
                                "from": "*",
                                "hashValue": "b23673e2da6bc6b22f37d233e2c165e2b75f669b4bcceba85e40d4d976132864e1ed99c99a0f8eff2e9dca139f0a2a51e4ae10676caedb22e9ae7d3890acb510"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 26907323,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "e8bc25ab2843a0f96441d584b468f6d98cb3fed5f891709725d1043158475a6097e36ad3d1253ef431133f3a5866a9457b15c64caf7f92c849dcc1a7369bebb4"
                            },
                            {
                                "filesize": 138739,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "e6ad477b79dd60c8965ae6652d6b3c0a698018647f0ec73e37f8c931d6938e0f342c6deb6e39523ceb393ef2ba74677ba59c2687d99718cc3de93d15c189ad2f"
                            },
                            {
                                "filesize": 44152290,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "496138d14678ddc43cb7204a8678be8b00e6d83fac58f25998c7b9c6b344e28a476df2b637d9ad1021d013998a5dbb22c8f5175ea462547056677f4b7d62008f"
                            },
                            {
                                "filesize": 39512477,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "67fefa8ffb199447b3057e14b024144162457ae8feb4d07fffe65075a0781f78fe826427ae8922634ca23dc74d41c72c8c7dfc8c9ffc406f3bdf016c136e6700"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "et": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 80889639,
                                "from": "*",
                                "hashValue": "74afbeb79fd3d7fcaf03c0219d55f1c4d4b6b5c0c82c2124139da0feeaf984c137ef928fbe407972463f19cdfaba73ecb9dd7a94953d3d5fe3c07a3539ef5ea6"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 39502321,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "c05761fdf51690f2c1b12ce263d6b9610382359a2c264a7aa7a771983da2571a38f34ecc11890be0d65e600d41ed38e8a61f094da27603e4dc28d56be0159303"
                            },
                            {
                                "filesize": 26899153,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "31de4d26eb2c9b94f8e2fe8a5d8ac311c4ee5beebf35dd456634c9a4b04ff942891028d8579b0fff04e0840ef19c8588da4992a18dbfa81ed914bab213a845e9"
                            },
                            {
                                "filesize": 135982,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "7258aa39e05fd826fd564ca5e2c49afff9938a37e23fb8431c3d772a96d52d4887c8d6c85c6051a3fc41023ab42cb70562f567b7e0f45f864d68c94da460cc35"
                            },
                            {
                                "filesize": 44092579,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "765ff20d5e48d2cfd824a9a386d21726cb75b63375ad1c95bf5b3c7122b5668a3ca1ef66011bf03762d7e6bde8807f129fb5449477ddb4872b320f1f461e1d1c"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "eu": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 80076462,
                                "from": "*",
                                "hashValue": "91659c6478a1514b4e4eee9362a2850f0d3718e0b897f9b3190046b9827f7b3e7a36d351858b28f7dde4da2f7be76234fdc5e5e539af00be3c2845ba132f5ed3"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 44137257,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "09c9bdf69694ba5cf5f6b19a7fcbe6cc48c2c318d20c55b2bb85d2153c78645339d83420807ee1e26de4be008a419d1faf9bfe59f842405b8b30e224972ac194"
                            },
                            {
                                "filesize": 39534632,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "b4ae1c85807ba84c46afb12a07aef0bd7c193df2cf16c00f8e9524d1762312ef21e3c208b51898c3a9dc6ba40d4f2dfaaf2ecf9e8b7b13a3efe428759f432515"
                            },
                            {
                                "filesize": 26907523,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "5de005f06936e93dc3b5b10ec109e705b3bd510dfcc8c791a5201ccd7e2d389f7ff6733ddcbc02895da4c1c997a006a6db776177c0d2aa4447a64e5f9c5add50"
                            },
                            {
                                "filesize": 131438,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "b86099383bec4519348e4d3545043b3ee2d82a2f5e427a4f4fea4648326e04468366875644638bcb2a0c34f68a3afaa7da33606253a9c7dd3c1cb026894d812e"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "fa": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 80133972,
                                "from": "*",
                                "hashValue": "0b0ef663196933d4842a98c1256e179dc0be7f44814a86a514dd6ffcc8dde555fe779a70fde6db5ef34005559d3cc3d2db0dd2a35b05fe0e0df8406d93eed83f"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 44239378,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "b9c24400bd8656e25bd7a81b24174e140328f7069d2ae62e32971446283b42f4d4119a4f44d0505026a4fff6fd94ce5a176f1fff8341a46e2d0ddfc377ebda1e"
                            },
                            {
                                "filesize": 27007356,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "bc4eef44343a1b30c460cc584b203c20fd15e4489205349f9c72bfec9609124ec1a8facf093e014ad7432ad675e6572e41bd687e2795a7b762447cb593abd5f0"
                            },
                            {
                                "filesize": 39668847,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "85803ac81f48f07753ec26b290ef7b4f9f72d6bb835df0c11f2aaf2170f7acd184bdc26feae4e0176015b1b1cfd6e9fe8f432a011da49de3bdeb0f7e93dd7447"
                            },
                            {
                                "filesize": 134408,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "255921a669a9ac9303d5ef8954fdfbb9a75017a4fc8f1f207ef84ffd0d2d39e742a5901d358fcde0961c99a572c3afc984533ed1918da8f07f88301ac4f97c91"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "ff": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 80068328,
                                "from": "*",
                                "hashValue": "f9b7feee24d8c751e44d2ae1aea3e3467a365bc99e79aa38b43e7d36e8d08300e98916547d8b4770c70f7090032ceaf649ee949a21f6e8c4fc06a4c969d69070"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 132653,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "afdf0a5b7a2052474fe8ce8ef6717a621eecc498cb11d789d37a2057666259d2bece572883e6bc2bcce1f012daf70a2cfbcc01f004c936ebc55e8ebd41eff28c"
                            },
                            {
                                "filesize": 39490782,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "2ff833fda086a85df3c00396823b129fd69abe07951a74fa8494d826519b3ff37b37576f4b04747fe4c193c54944df2340fb6826b0d5684b4a914bafe3a13046"
                            },
                            {
                                "filesize": 44085544,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "3ecdcf16fd70cd7167c2b9a4dabf3d59c5dedf41273f12e2a2c3df240faf2b2ea8e546174a703ec6e18f03b2ad701923ce162233b828f431f5145d0a3f4838f0"
                            },
                            {
                                "filesize": 26890833,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "3b14a626799efc9c2b18e9b5c0bdbcdc75470ec282ba32f0e2bd4d98b92d7976db331f88698ec645e260523df876cf92e62cf5baf0387ee8e93359f1cea73caa"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "fi": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 80051931,
                                "from": "*",
                                "hashValue": "27f89ece47a7ae67fae65da04d683aa20a7440f6004be286ef4245f0bcc80656a2b2a6df94655ea4384e2a26a8b454bd2b7eb926ef3768ce45b9829cc933f8af"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 26896361,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "5e6a48a04673513b3fac2624142947805c5e07dbbcbe4ca44aeed447377feaacffa368bc0a172f458eb9c3f30c8d3195c22345ef55ed240991ca68b1411103be"
                            },
                            {
                                "filesize": 44085629,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "1915b189a975fdd5ffa6ec705c431ba79d608d500e079a8a6a9b0e93c41df2a2c5dd5df82ef4ce681ccd6d6a2d0f4860ca9792462e28cf2a025dd3bc291d0103"
                            },
                            {
                                "filesize": 39499650,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "a242e21cf08cfdc5523273bea82baf97b47ff2da9c3199c1c35794d584619c254e3fe7a299e14e99ea6b046652d1e54b5280aa897cbb6f7ab9a4bbd10a6e07bd"
                            },
                            {
                                "filesize": 136389,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "2ff90886076d0abfd041c0e23c024faa5d059709b232a14c62c9a4d4a3abd58293db6f4d5258ebc5da6bae8a4dda4a02f6bac8f52640882053c034fec3fd0c34"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "fr": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 80440257,
                                "from": "*",
                                "hashValue": "f467199a2ed35864faca891ceb61f4cf8eb42be38fbcdfa6115a9fb18fece5db9f033505b908cafbd34bed59a9e852b1eb985eded76daa6b8938aed30de1e568"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 132094,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "780a910cfb0ddde56d8dfae0830df15b9e8b47c9d69b0ea5454299dab465b9dcbadd13fedc7d5f390852ad383ed46f1c4b9544f4aac6fcf6a4dea4a632afa510"
                            },
                            {
                                "filesize": 39536188,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "0e9ef1df9768912480de2dc1b8733c24b640fdb600af28fcbab9b2ce467071a309bed27aa5ce9b59807fee64abf9452b58d87097a6bfa77bcadc32f930c9e70e"
                            },
                            {
                                "filesize": 44127526,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "986603eb124adf60cf3deabf97634333acac82b151d0d1309e4d89a41b81b199ed065b71b3f4ea82bf7887c8d46da2fc625dcaffc5d501ee3b07af674b5eb1fe"
                            },
                            {
                                "filesize": 26932428,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "6dc9dc886809c61820a83dd8bd4d029df822863c062a008e59d9d5a086ebe4edf44496309afd488919fac99aef839f08530a5106e9fc7f8aa1661398a84c973c"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "fy-NL": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 80062385,
                                "from": "*",
                                "hashValue": "ed3a4d3258e3a62ac2b0a6634561a2d9ceab9176de9e6b371657de53b47c60c17952bdcf49461c0741df2604ce52559832702e8b90e8052562a98d5906226e70"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 39507528,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "b966b3c40b940f8b5d7e53435b7d0f9ce04e8f551c5f374daa94a112e7e9ba8af52bf8cf8084c2eac2b3c175bcce2f4d21345a4238b4d5ec8673067af3dc801a"
                            },
                            {
                                "filesize": 134164,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "5f0b328f9c7e614327149b438a43bfe4a6c8715449af0b095801d824f79f7f7d20de5056882f56f7387c3531f17b9103e22ac99e9c07362771a465dba7bac051"
                            },
                            {
                                "filesize": 44103869,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "eb43c3636e845eb480407f7fc6a30ad02062b022142966c8ced4ac942849b832ed9b89fd2d1268126416d1c0fba1a76c3f024f8e66cf7b81489a3e87e5a5a799"
                            },
                            {
                                "filesize": 26913795,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "1baa27c14989ffbe2254f4b57b28407eef5eae54bef5d755577e038a4100f898ee2adda75b67d5c8fb1555fc9a4505cbee4d41f55f7fca0112cdb792c39e1e27"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "ga-IE": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 80075722,
                                "from": "*",
                                "hashValue": "6bf553847cb54ebca4ea278066a066c3597255601b7319b716a56a88b9f71cb37560b5d1a59ab98f44fc8d438001d4ce65fa4e772e8e6430394b9d62e540d33c"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 26913884,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "015bf6c340a5224189b2a1ce2e8a20972504c0a50593bea7c11ac6c515bbfc5b5db92742b63e7ddac649eb2b5c19c8682b6c8df5dad1382a6a544d537be6d5d4"
                            },
                            {
                                "filesize": 44116404,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "b57a8da0a437f9fce223e91775ee982a2db3519ef5f4fc736273f03e201d98a88c07cbc1c5f1a98e035747b9a303679995aff72875e9400dc5e778030a6eb8e4"
                            },
                            {
                                "filesize": 132213,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "39f3eb95ee82db795b19aa9be55b009f70ecf605848d3aa153fb23af36c0aff3e3dcbd19fe3b89d24e31aeb3ac001aa4b2997dad205ebb640184516ba8f8b818"
                            },
                            {
                                "filesize": 39522742,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "ff5db36847e52ac8f5fe69ec890192740437bd946bcc0755c147bbb0317fdf0349a9b85a9821f301bbbb655592b993579ba370c10f38611b0aee32498d2beb45"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "gd": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 80067475,
                                "from": "*",
                                "hashValue": "f0c5e04ed13e0313f7089c962c0b613aa1c1fbed3de55f999392e30e6662a9c494fb4b64626ecbc726f36fd044537bdcc1d13cac5df678ba10b90ef647d0fda6"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 44102053,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "701c664d1a48e270e5c4726d858d98274749f89aa9ea9d7479a4f77a727af2966c1b61e68f064f0e49f12113e0d5b2e0ec9a0a0d2ca28146bc389c18390ee049"
                            },
                            {
                                "filesize": 26907224,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "e038fcf8dac175b720a94e11b56fa1d60ac0a5863e2246adad5b07cf0975b0995580cb52f99de2d8fcaed5ead5bedef295df8dfcfcf62e74fb3cbe12ec54bbf5"
                            },
                            {
                                "filesize": 136330,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "74168c1cd855be2ef9fd1a2368dd35214509202e2fe52ec7de9df20d15e08b05043d24d6ffef480830279b258ee8281eb7a92dc739326d05de15e20725041cae"
                            },
                            {
                                "filesize": 39512199,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "e6198a3afb160d261dbce5d14bdbc5f09c6aa12b109170f7322a64618fd37556d6e08ebd8d628621a24112af7952e65efb4c3127e09fae1640c1d534866ac289"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "gl": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 80054066,
                                "from": "*",
                                "hashValue": "ad9a488179c0fd18419bae60daaec799de049a47c7523dfe4a0f77a1e5f73abc302d73724fd60b932ff896605dd176dd4a18a912566f0854966bdb4130400075"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 136054,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "30f8fbfbf45d7524d4f6e8b8276b032ed62bff930510fca4d049337490348f1ee4576d97d7c177e7832c324d2cddf3eaa216e5982e3a2744c862c74609b7289a"
                            },
                            {
                                "filesize": 39615676,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "821b3c803b1f2433fdac91d243495168d78a65cfa2fd63b620936b0d1946de9f489cd7cb302f5498e111ccb3b895f3ccfdafb725950662bbc61b3f1b604f9017"
                            },
                            {
                                "filesize": 26905573,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "ddf029f10b053d9784e8610d773be3fd28e7fcf48a036b709fc6529e49e4d8731a5597392bcb9cde8677b84ed54740f5bb08e45590154ce1d0a4d01e02c0719a"
                            },
                            {
                                "filesize": 44177857,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "8b8919835c444114370def8e9a4a443610b55207230a6bac7e9c3462362d5e4aee9ae98de9725641fc427282e557829c43aa4f2bbceaa1c00692b86f316931b4"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "gu-IN": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 80093900,
                                "from": "*",
                                "hashValue": "111d0cf0ca1f0260d7204dd1416f509278c37fce2828ce1be521f3013811df424f798b75ea9115bf817ee46a5c5516cb152140beb4f8f388ce6a181f1d821cea"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 39483641,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "31b5b6039fb5d43c0b4413ff17b851ededaf299e6750fa4d70e5c7f949e44329daed69a53d5a19b511d0c8fc6d69f8a0395ed79ba218f146c28313b7b286e663"
                            },
                            {
                                "filesize": 132544,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "ffd847395d8931981e7a90080f777db2782cfbda320b3b42ce37b85f6f95871e6602eae76e85658749f603fa47427fdb716bc78d98e599cf01fb0cd38ca6faf8"
                            },
                            {
                                "filesize": 44080737,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "fde7653406de3479ff072afc6b06a53fbf0eeb2c2624b39301f17a1c4d40b04993eeb0a93b120e5d15b5adaf49b415c5055d8505c803909acfa957743f02d60d"
                            },
                            {
                                "filesize": 26899538,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "ab6f28d639be3896dce1dffb77e2326b8648fa441f5cb74c8920df08b88e66e769faf1901266511da3588bbbed14e92c48d042693bf2e492549d51f8bfd09db5"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "he": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 80085117,
                                "from": "*",
                                "hashValue": "9073576e41592ce8acc80f38e8d62702bdc59db2fff84455618e32549141abc798399006e67e56ac02487328b50e9630fd1d65c88da66b901eadc263e930509b"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 135108,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "58d8fe936eee2d53ab33db9d6e03b5667e1ba34fcea59be422f0d31f1b5230b6460b7e63a42c80f92cf8e98baf9c4e056e4dc8669e3152eafd6e65b32bd7999b"
                            },
                            {
                                "filesize": 39663178,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "cb7d888177d1f226d55b19ca17f4779cfd61bf75bfd4cb7ce27a511c0f0256a6505ddcd07c3bd5ad63d28a1191f6b97affeb91e183e85731e83d65ecd40bfc56"
                            },
                            {
                                "filesize": 26908739,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "881652cca3ea0604523a5d7ddf722def300d0a6886ab4c6d931e057e686f6b5e756aa327ef73cb70e82607e7267b4b6577fda56d44085519c0f68f0abc252684"
                            },
                            {
                                "filesize": 44240442,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "56b70467a838e355db9253e7d07b2b93b0dda8787e0b0bb930cf3cbe88fd63302c660b353191af32c47aeb3e5b3e0217c1c9799bbacff0fa364daa1918b0dca1"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "hi-IN": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 80119785,
                                "from": "*",
                                "hashValue": "894702e7ca2fcb305f03661587d1a1987ace704bf3a2aab8b0d5193191dc17c9ac2826108a89701286c26aae087e100070efc240cfc0b973757598331446f8f2"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 44107355,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "d453c0873909b1d431eaab350ea3421adc6eadc9a1e178b37c3c11f05f4d2b1e207ea58d5d86960a0cb7d4ebe74e2e0ce4a76c82bc0a9b1248d68f9dad6d4a7a"
                            },
                            {
                                "filesize": 136480,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "c6ad6c3cf8736ba00fb5b10c6180256e46b876c2d3b4e824bf6051c09de34b573d11c59ac4665d38ff0588e99f0eecacb6efe65a0115744f2797c8d585d35bba"
                            },
                            {
                                "filesize": 39491863,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "a66bb826984c976fdcaebcb5b169a2b746dcbc0335aed067ab8b4245cd6428722f37d31c7a856e8519f361f81d82d111b04886a30388cfd81e6677f70c01eacb"
                            },
                            {
                                "filesize": 26903495,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "251494d7bcc782a94518ef9e0c6fd42ce4a156e4927e7ea8b294718f1a989cb365a257ed84a344138e2bea5aa0dabe865bc2b74441bdf0264a9a2f27aa9c65f6"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "hr": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 80091056,
                                "from": "*",
                                "hashValue": "8076c0bcf22d3bb6975d3efa14ff8fb20cad725976201c1e6503a84dcf874235a07aba24d5bba4b974705d5447d9445635d1b9678e3dc94481ddf8dc4a533ef8"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 44142450,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "7cf85034fbd756b54ade7ec3c224d78c51b1bd98e4380eab0e2822f2190babf948d3d77b60dc124cdc55149b8a90769feed0cc66eb09de68f100be06d1f7cf03"
                            },
                            {
                                "filesize": 26907481,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "81c7079914eac9db0deb6bfa0f85379d7989c5e02a9098f733fd2537e24788d881c579ea914c4de6e7206fa7f9eaf1e7c962dc2eaf2b447b8e2c2eda5a98a146"
                            },
                            {
                                "filesize": 39516750,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "b1caa758a34eba7ee7b32cd6b130b64849afe099a89b4dbfe7085aa0b33805fcf79998cd70a28e8eb2a12753b17320e07714ed6d059dbc804ccbfed472f469b8"
                            },
                            {
                                "filesize": 132081,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "676b34df02978b7d0256608d26e55a500cc25660bbb8b5c95d2f97927b1aeaa459f994a8bdb9901369fab774f1d37ad138c341dd03f95f2b36604a601d15ff83"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "hsb": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 80075379,
                                "from": "*",
                                "hashValue": "c0d8a7cbd48956d27ba4fdf15bbced0e46c335c0a12179b762cdc72532b73659e3c0ff526178399632569385cb0020f669f5f2c18c3cc8099b023e23c9653d81"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 135611,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "e5eb7bc44d0f5e1c3ca207ab63feb757a66d0f1949d1335ab673e490870009840833245825e706ed88b8bb89734ade5727c14b147bf66034fb3e5e4f9471bb26"
                            },
                            {
                                "filesize": 26911112,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "3c18584d4ef86b7c2c47086e8527431da0e67d7f8f9d63f965020262d2008cd8787f2d1c18822cacefb0554ed2e3d82630360703438439da0ffb55859ba09b10"
                            },
                            {
                                "filesize": 39526446,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "90353b0bbb8198c9b930754943bb4d279306c1301993b397cfe21fac3489274dc8008fa84b7c903abed9e9ee3c35476e6dc8bd5b38a40f5181494a0229cd0c60"
                            },
                            {
                                "filesize": 44128404,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "72356a00149897e64eed37ebee17d7d9564861c62cf2ad3d3ea159e94e1b97759a66c7290ebc84cbb75900a2964cb483240aebd66b5aed2a277d955f9ee8a05f"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "hu": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 80691600,
                                "from": "*",
                                "hashValue": "81f649d406602dfb1a6df982ed0c92dab681e49801b4feea6fab59077cece23a36077d90b50091f2df1881f56ff742ab0bacf4f95e70892bdd72abcbf7ffa0f6"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 26907881,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "0ba1315aac86a9919b024b853f56c9c69506396995e15ef4239ba5032ae57fe6eee78d3231589db38a0507605397b9aea46569eabb83be6685aaa4a8e7da5dc8"
                            },
                            {
                                "filesize": 44108747,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "3eae0ba18014809344d2e99c3d155f9219313f8bdbb7cd79108c460dc619e2c7382bfb4b2bb3fad815698aaabb7f8e400c7351b39a6964ded1b345ebf57d4936"
                            },
                            {
                                "filesize": 136028,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "09bd6b84c656a24b8475a202d6770ea5a47d7f2be0f08bbf513c3fdfcc1f94f028491789f22a3f0d21b2ebfd3797e06e239b8b44308819638e04b4f4253e2de0"
                            },
                            {
                                "filesize": 39510732,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "16da25630a44a0c049f6cc69e669dce5455eb4dff2adbb5593994bf8503ee9ac3fb2865dd6182c049bb75659bb36145e6ed394ff74509995e423aed26ffd7311"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "hy-AM": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 80149523,
                                "from": "*",
                                "hashValue": "d718698c1b81d57b8eb4e683eaa9f89f702a7a3ee786df3df42a5bcbe9055392cc853ae46dfc8ad46203b8c188397ef9a92696f1898ef9677c2978a1d3267300"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 44202701,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "438373199ec1052d9da435d3a44533a8890aef7f0445dd0a832a12c5d0fc1a1d8538cdebbe9ce18b05da0362d9a2ec080679963afb68bfc6f750a802c162f499"
                            },
                            {
                                "filesize": 39601467,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "4739adeb38f88dbab3d5f31b01fcb2755bbb423b6a10de6a106d63f94e71ee86299c9e222da4698e0ea2e5d951abe1537dcb10347dd13f610cfa7df358130faf"
                            },
                            {
                                "filesize": 26890798,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "ff5280f5d48fb4497a59abe08e9f5c18d9656db54ca6519030d939f6466f8a4ae384e4364aa2c7ca78af094857983182b26ee76c9cf268726266b652734a4a88"
                            },
                            {
                                "filesize": 132065,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "29b3ba4af0b466d94824132af625b1e4c1453d252ccd7dc6f16e7165dd612e64b1bc8e9f225d3ae80e585860268721fdaf2c4adcb3487cd468ada83d1e0c7987"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "id": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 80135371,
                                "from": "*",
                                "hashValue": "6d6e8de8fbbbcd42fb00cecf1086ec035b5220f1b8ca622137d3298336281a44116b28c759c49281cae5c90a372fd59df6df542a621d0b6499bc6c2b64f44ca2"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 26889399,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "f6cfe63eee74db6e866406c4ce447e3a8c50391018a6223f2e78e5ecd6624952478bb70a86c221c7f50f93d60140afd92bc2ad241ab7693aa4910404ff384b0d"
                            },
                            {
                                "filesize": 44107714,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "88a1b2afe4c7b447d2343538ce1c60a94cb7c3a6666b91c8b13cf1f10430f12674cb9bf797366a2caef3176c4efe01c74abdcf3f5fe6a5972481180b4ffdda78"
                            },
                            {
                                "filesize": 39513428,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "af16ca6aa0bdc08dfff87aab88f0d64fbfe70364e826497a9cc5f2a8cfa2a062a84f1b53d11f967877cb521b988a81fbf845409712b6d8a60f7c97bbb6edd3a5"
                            },
                            {
                                "filesize": 134543,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "bcb1e253a65023f095b39f25dfcf8f7560b804196c9f0e970a6fe77b33a5af7a44ae699fd3c6e2997554567d28d52038beffccb541610ed31f8f3ea08bee0070"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "is": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 80095318,
                                "from": "*",
                                "hashValue": "faaadbc35bcda43b54539c692c0427d6889f330e9ae5f9984469e5b92612fcb9ae1b5b7363409c72b7ba47d27fe85e4ad5e58971ecaf6c134134e587e1be7362"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 39515360,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "7d48a0606d01ca3c2206dabd22cc8197dbf6783c356fbf2123377a7e9da05d553351ef4ea5fde0d013f3e19dfb9aa90ce23bfb89afaa45aaf0a15cdb3d593102"
                            },
                            {
                                "filesize": 26902105,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "fa7122198f271e91afe5a3e1c7cf2ed20f0932af63866cecba7f72dee42d3cd720cfe5773ca8ea2a430786ed39f115db7fc6b06622842e7023b0297499053f0f"
                            },
                            {
                                "filesize": 44113223,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "6b98d46fd7e530948c359cdeb285688b47d996a851dfc53e92e84e5df4dafc1bfb6e707e20d8566d40a1c93acc4962da441797d5dfe2a705557557808253955e"
                            },
                            {
                                "filesize": 136979,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "b09424c932b8137888340c7e465a88e26c2a06d78122ebeca1a86051deb22776e8889a8a385ec8fed6bd3267ac2457cca69ee560027adc5059d7d3a1d9984e4e"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "it": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 79966457,
                                "from": "*",
                                "hashValue": "64ed1fad67b23d00ea1bf75b4758f7563f5270aa6241df9d5035f85ffcb273d0cb61f5670dbe644331c2b32c2c26d5edacb10171343a78533a21fc2b5eb3637f"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 39461907,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "e96b6fee961015f3057cf236ac1f5fd17a82447a42b2e251cecc7e3c12fa632eaa34943acafbed80af7af984415275818873ecfa570c346c5e6d6355d5de0c27"
                            },
                            {
                                "filesize": 139363,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "4762fafb39d4fc5fe96b216fb0316e36c2cea90c5603b719d7f972adf79018e5ee3e0fb790b6c916489e363f93c13961362eec56aa5afa39dd32ed3f8c7a01d2"
                            },
                            {
                                "filesize": 26864140,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "5445da88394fc15651e6163ee9569f50f363e1e92f7f62ff18b0700aae831241194f0b0beed42ef427adf85ba987d329f89651ae8689f2f6e274046dc987efc2"
                            },
                            {
                                "filesize": 44039840,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "802eab858817cd0ef3832974483a268030f4a1280a760e055fb21c5c421eac76fde8e7e15b130cbdb6924b11ab65538c6abe4e9d833183524a92b70bbd88a5f5"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "ja-JP-mac": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 80326878,
                                "from": "*",
                                "hashValue": "44e9010ee4c449ed10655dbc77aa97e4a78563f0fa80aa1e15ba9f7aa374d9ee6f7037135a04d3238ae96b85af7ce2986e57a0a223ad860bda036a9511a7deaa"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 26912171,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "b943097eba6d9899e60d30dde1543cc9ab09f2a36cc0c61b76d27ebf5f6ffe2252fb0dd6b53720f219c45b3873e21d4b7cab1a5c41be3452194b48d9589bb003"
                            },
                            {
                                "filesize": 44114901,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "e326049222424d850e2d4082b75e9abdeb86cac53c9cf36ec3dfcb83895c6388ec908c4e11194f77b2fba9a886d113dadbc638d2fad9fda8090a13b2ac41bfdb"
                            },
                            {
                                "filesize": 133916,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "8b7835caeb35f17349e04ef39596d7910e8f1013547ded752fb4fea798966789cf211b3fe87c6f9cf4638cc7f48112324b214d4aca4997fd2f7f417aa519e4fc"
                            },
                            {
                                "filesize": 39528027,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "511a5093ff2533d448234feefb9e821889d5afbc93cdb3842a404872fff65b21ba08ed4673cdade28940348702e2a97638e23ac84f6879239f00df0ce2d0eb89"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "kk": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 80117739,
                                "from": "*",
                                "hashValue": "a9d808ad0057747cf59db4edf5b4027f3603b73ce06f2898c9267aa508e9d16b55b566eddd35df25c4e8569ca92c054f4db08f4964921508885c494ebfa0de62"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 26987425,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "c59a63847524def0f99c717b39aa835181cd0922edefac67db2cdda46c9456822d2587097eff02cd0f1bda03655857c69c1224cb9a110e5376b0222bfbcd0026"
                            },
                            {
                                "filesize": 44184963,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "4eb8c4a1a9eed34871ebbf8eeea6842e9023784648cd3215e4f76f829943428944a56c52d02e43e2852ae39dc25b793f41c51bfe0eb69bec1f534ae8dbb0b197"
                            },
                            {
                                "filesize": 135313,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "9f8d973237f4221a17f6296ea2e508b3bc83a01a833298189a10bf912fb79412dbcb22844bf1b477c048d57434f77a9d8e5983e6fa44c3a2d237b087b7a0fff0"
                            },
                            {
                                "filesize": 39601818,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "7df0ce143e88b9d00011be9989e51248ef9e959f25e9594ebeeba9c0fb14c7cf2456f6157485a8b4a5bba8592c7f126419d5211b69176c396bb02f1cf8ec8e7b"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "km": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 80415307,
                                "from": "*",
                                "hashValue": "e583f78cbf2d3fca2276d9735703d7f6eb41ac4299f6645f271df4a008cc93360e8df1e2d95a7b5d29962e4d78c24e19e61b9ca47e0d625cff12135d575b7bb6"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 26928576,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "e4c53dce549cda5b5c42fec03837601d7e6cb688d0982bb24f4a4b7fc1e8c7ed412f211581cc030dc8f99712e873044ec3fd399a4cf232a3630e69eb4f9594b2"
                            },
                            {
                                "filesize": 44242466,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "7f9bb1aeed8147ea9dabd960a026976c616ef86d6251115686684cefaf80d1bbe42d54b59f3b05aee9b891422576fde11c05c4df5e05a9bcf8a3e49e02f46379"
                            },
                            {
                                "filesize": 39597780,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "8a4a7e9fad0c2450211d86b816cb6d399000d8dabb2ba29c059c633a1b421e7c181e44945303eca3f20549f45971f71929da5904f183210d79621b8d696c0520"
                            },
                            {
                                "filesize": 135951,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "8144de9e9068358637f3c48a7e48462431d9d9572e18766e35db398c97e56697cbd5001e51dff27a993d85fd8e5a80dc0765e40471ae99973a7357454a4f0bee"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "kn": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 80149979,
                                "from": "*",
                                "hashValue": "31ce8ebb610f5e3e41c9811fff47d16898628d03d727f34c3e85675cd079ce6399e11e9f79466129f075adfee255603ca77cb433dd995869c2ac2c986eb73f3c"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 26911458,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "bc6d3de5ec3fba018108f23db0717a5ad0bb3cea3ab382e546e86a0853d100783bd032c44a81e1f9cd57f0db47ca7d18a4d03870ad3f9e39e1bc260c2c029e05"
                            },
                            {
                                "filesize": 44157303,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "9aab692294f9a70022fbfba46a21faefb2367954f132c7bd94fa2dd83fccd2d1ac70aa646437022aea0f58a37a19e9f532adc1051f1ae47c604df18bf7d558ad"
                            },
                            {
                                "filesize": 39555723,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "07f3c4a6c1d99a5dfb4cf68520c3f6df4f454b4ac9c6216d13c7dc14e62aa11e4b7be4e6ccf3786e4be90daa52a5a198260967969835f41679fe227c49b809b2"
                            },
                            {
                                "filesize": 135497,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "ceb45cc24ad19e8475f0fba2d6e62edf28c82a7d107d7fc2666cee54a0e0f25721a9dd3e26baebf991b30db9ab5dde934bbcff44d5eb8d0271a959506dab2f6a"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "ko": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 80080310,
                                "from": "*",
                                "hashValue": "65c29d79c66ffab38a6b3abb5eefedab96ebf33579d3e69da3bb40076dc7812e3e56d4bbb30589941eeb274bbfaac99f91c7cce124296eefece7cf2224475eb9"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 39681098,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "65c692c3f681d010420250694b1e76411ba6ae8ff2417b7567425acd8f34208a14386e0e573cfab02844537f691ce97f39445c97222a80826203f27eb8a9412f"
                            },
                            {
                                "filesize": 44247320,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "c7e56e85f5a712bf0ccf62029253864ba9a9522cbcf748aa5cde58f8c0f8523857704a6128aa26ed6199da63a1c7a3c2ba06515b27c39219a361e220ff45cc73"
                            },
                            {
                                "filesize": 136164,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "4b4c13fd3b1da002622aa9a6b6f58b77df7eeef47b80237bb3c57003d1b605491b41b7c39ccd9bff23376deb7b6622860ced41681bd0659a4e7a50b26f0b8e38"
                            },
                            {
                                "filesize": 26908323,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "7e275f928379a2c579da0e793eb07314a6e781666f39ddfa556d568adf3e0e906509187942af4fad79516a9c079438ee08f98cfdb4adfac64c52df43f0113937"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "lij": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 80237762,
                                "from": "*",
                                "hashValue": "eb6f5685c98a26cd45bf3e470aba4bee8823e361089b0e48b5a6defcd9376e4725429fb149e4f17a7769ee78290fde1e7ae54b24970e8cad6a9753788d606860"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 44238177,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "012b08d60a7674b6a42ebb8a2fecc2649410186b5b76e229f7fd15496281fa92f9f34d241dcf45d165508abe1cbdfc30c453ac95146ce072ae17ac649fa1be9f"
                            },
                            {
                                "filesize": 27117577,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "4a3c46b07548bb0ebee1f27d8194e9c65fee07265c8670e53e344ee8a0ba199ddf35a9fa1b7115845c55ff7219c72e96572ee483c7fd2cdfcd1084537c35c003"
                            },
                            {
                                "filesize": 39677778,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "951600c4f616c90d69387a25133720aca4a7527723c822ccb12c1fa9066cc369bb389d1158b32267dcdd51d453467b53add224a1c13cbea32cc0c067f2feb0d7"
                            },
                            {
                                "filesize": 136756,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "3bc136b4a484c04232b0a02510ed01371aa417da077cfb076b44b0443ddbdcf6c0e8d543d3af316ec7fafc9fb9f89576bba28c3eaba0e1f74f2efe2e5fcf8b19"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "lt": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 80420576,
                                "from": "*",
                                "hashValue": "084cfaba64dccd061bbe023335741935cc6366945aceabd3d60a8d0386bd54f297640ac998fdbdace1d10be7af87890704527962523406a655c0f8feeeae56d0"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 26947230,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "f759b9839dbe8bc2dfd05852f6a4005278117210575db4115e939ef9a3d31b9f9c442375ee7bc69b8da1f4e8bb28c7da742d558a252a81ae82f79e0e6214ce31"
                            },
                            {
                                "filesize": 44162466,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "0d8397906ef3b41ab46464f8ed64ef4b0e399fa314b977f25b38e08894fcd0a9269b8682c91a84f9f214b29156c75e6a02efc5e30ee69228ef7561718f145399"
                            },
                            {
                                "filesize": 39593044,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "d4f742e0e42e7e21f3779f759e7cf79ab9b386762c55be943e28e506ab9dca0e247ce03f2da00ff2679fa07f69e9443659ee02f7507e141d452f8491200c0b79"
                            },
                            {
                                "filesize": 134354,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "083d3ebf07f351ce968ed71f73c6d6fc198303397edef6d973aae79725fb3f44731439af4bf406f1450e8bc31902eb5080b5cb94f44d1cebd3501e4bd79b9dc2"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "lv": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 80365502,
                                "from": "*",
                                "hashValue": "edfb9f29df80aee96cd248fb0e7f80f0b991ab3498faf4806f7fcf67f816182b20c4c6eaf1c69e30f94ab15df2359f672ca901ed33739da49d7033ec51760e9e"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 39517188,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "40eec5d431f85f68b392e62043b521ddf830beb0e7e458619c77dd64e1d6b8d5414591d2379f07a7d0b0f114336ff12a27cd3a383dd199a93e412df7a18c95bc"
                            },
                            {
                                "filesize": 44112465,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "52c39a9c4514fe36225b49fbf503e94eadb85ef929a36e66e1ca2eaaa13a4fed3d784f1de802a3191648ac3ad403d27e059b0bc08d37122f1dd1d5df2ecf448a"
                            },
                            {
                                "filesize": 134390,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "c59b4ffb270d1469d506b3b17c818f50b466c434583a41f2c6569b107048b38b929ad8df81f658a8050ccaf2435717f65388c17110615cb2b5526ad0dd873534"
                            },
                            {
                                "filesize": 26909235,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "0efd1659c9afc3332d1c9fee0031167af8d56ced34e12547d52fb39de73524b0c3d7027c471351abbdbcb72189ea0ebd0b5d1df432f54d23f6d76c9363be9cbe"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "mai": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 80129013,
                                "from": "*",
                                "hashValue": "fee7abf88ed1826f21f45de3bca5879772444974407d665be9379fb83f47fc56a992fea2eeaec6eaec7f5ccfe41ed51ea479befd4a8884b7b2fb20d8137408f7"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 133384,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "045defcd1d4a3767ccb8c9de2585883dbb10d31f2e1365ab764418bb7a67787ce69c7f532b424e838b024deec1380804503868401762f5e7223c848b3e872a12"
                            },
                            {
                                "filesize": 26905949,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "136eef1bfef9074ad9864e8aceae29a07ed59eb87283f48656b41ba9030c17ac869b3c6124069eb5bb0369e97fe59b34fa4c52f0b54779088b360f93d346ce6c"
                            },
                            {
                                "filesize": 39505622,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "51d0783ad1add1c1f3bb22f31b50770323b67426e80247c3ccc22de4860e5700d821069e1857fbfc09d93433c66b5e01633806fb46edf472b0de95928522a5e5"
                            },
                            {
                                "filesize": 44104866,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "5a7add73c012801a7016e6c9dd37be6f370e7c191d97186c65f0a0b5c358bcee830dd64a57f029aa6631e88c7d538b593a904422350af3857fc5817155b106d0"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "mk": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 80861830,
                                "from": "*",
                                "hashValue": "5562d763c9d130b8943f0cfa5d1f75162f8d4f3dd74c99c0b40c4d058778282771ae4bf469936cf1fcc8edb6c034cc872db46d91656595a91c60f1f56b53fc4d"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 26905564,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "774e5ded5fd25dfe02aeedabd972891799b29dc8c256a32215777dfa9c9bb9b8fa9e63173915ec7a65dde35274ba15280e96eab3e67625d66e0eb844b2bc919b"
                            },
                            {
                                "filesize": 44119831,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "6a11b1a3d40723655e75b507cbcdbe6dc05530a7c0a7cadce4622cfaeef4f8aaf703d55298dde7dab274daf6d4542212aaf2befcddb6b29c224d2167826b5b9c"
                            },
                            {
                                "filesize": 39512558,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "9d18ca5f8205af83f6d62a08c0b3b0836290d08a39611fe6d9c06f4fcdd2790fb3b7aba3e3fdf9c99041a8f8559c8c74b17d459bd0c307a4fa01ff6c4464e519"
                            },
                            {
                                "filesize": 136379,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "e0b74774e7ddebe02b6399ecf5e0bae73d131741f6669063a951d5028e16311420e57a33be6f2fa77e638ec9a923ecd501752c00caeb8ce30c8109b1096d1ad0"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "ml": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 80136416,
                                "from": "*",
                                "hashValue": "2844dabdeeba76264713abc1c492b24b803d6808c030d88298da3e446ad81460a1a06339fe31c3976ace8d133f8f12c60ad2b4e8ef99051b4210b733ebe343f3"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 26907111,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "0fa1008cc2b35a53efd474124228ca483b98dc88c7e4d9b1295585eb213f5d6ede7b74ae05e210c98518cdc8b57b9bbd35b7c5555611c4e8941a1434184ee5c9"
                            },
                            {
                                "filesize": 39675623,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "7d1d936551e0b73c416c85d6f11c7e26b1601877bc2f127885ec72a1736a8a4fa9c8262f699ea04c4d78360e9a74123949dac5ae17d83bb9daac14f4e77eb031"
                            },
                            {
                                "filesize": 136396,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "c36370cd2fb700ac1d027a2f5a68a808cb17c443d4fbd668f3ed19fe9f75aca9023f629cffb6f364dc1cecf8ba50cf7a4ac0532dadf0227fbc825e7979701174"
                            },
                            {
                                "filesize": 44234789,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "d68df0cef36dae709c7f2f4c4983f07d0f6a56321e82960efa954db46fde4da08a724eb6f5e5d7c90f65fb689d7054a3e36dc17ad2c7b6ee4380e9e5eef07e5d"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "mr": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 80128227,
                                "from": "*",
                                "hashValue": "eadb793c0bd1187185e419f4cfc54f9c757375d0aab9db4e0dea5df6b75f53804d8dc0efe229e9d7c1ec3bca95ab956a76b846e08505006658ed0a30740b79cd"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 26911863,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "1163533a91bc88488a437ab3857e692644721d4e6ef7367ac8048be41f84b60cfc803e85e3754c0d7af4b3960b35b42256b97034bb7dbad5191645fa8b035462"
                            },
                            {
                                "filesize": 132533,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "92a21d140a0ee928a68a95e43e1b8f0962c1f67287e3af9f16c37d66f2523fc84d80aecb021e9d32ffa219a3bb8be0ae7316e292efa497f239e11b4b40e5024a"
                            },
                            {
                                "filesize": 44228969,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "6f8708e4388bab8aab8f177a6212ffad8dff50a741a89d919904d5075e14bb4c9f7b6932e4dbff122c693f7fb84c695778bbcdcd1455202f6646a0b86e47dace"
                            },
                            {
                                "filesize": 39666801,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "f08c33f05430256324accdb5a5845eb63eb583e01fc538c46020ecdc5940902f98ed9ae0769af0148593809e139752a4865e2e7c2fbcbe53dc6e9ee377e852f8"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "ms": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 80101370,
                                "from": "*",
                                "hashValue": "9999f1afad46fa37ea5e269b990b04d4ee1cb9e70f98d858dfe29b62513db66960f63145087f6f821372d387d6dc04c873c90c2bbda2d5d8880773d946abc4dd"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 137087,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "c8bfc7e5772cd565c519c2d60a9215c7088732e6d91f5bdfabf5238edc108439b287dd5122a65417b912cefbe769e08e640c749d566a3bfe28ade424b0d86716"
                            },
                            {
                                "filesize": 39612903,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "49a6551f9f4f445655f096632cf79933640c400f1b2327307b9e004c924e8cccbb331c5fb37285a73e26ecd6995c00a4eebebae96a36f1fa9b1483dc4cfc838a"
                            },
                            {
                                "filesize": 44177635,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "d314e3fb2797c0fdc16dd72e59676f3c2a44a578f5c22687ebe81f91e18c85506a1c5858193e1328211fc41088847bf7591fa1103240576b0d1485c6f9e68275"
                            },
                            {
                                "filesize": 26883541,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "c14ac0839ce4b865fa3d3488d36b0ce8c4d0ba17227127a7b16171feeacaabce2e0c2dd705d4414aae64c24888b52a94677a4e74c0b65f4ff1eff66bc78fd26b"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "nb-NO": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 80054483,
                                "from": "*",
                                "hashValue": "926427a40f294a7047839d1d7e5755f8a3e4928a621fffc03f3f1a4e5a18299e5c7fd32b59ede80c2c96df704cc4e0f9c7ffd03bfba4ac15c3aa596fb7d3ec5a"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 44092616,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "eab9ebff0e82ccee2309d193d1648d393896a2f9738612b0deca0a1146183250587b5d943f0f8c4e04a64e7d96305e50ab2d2b76db036239256098a9c2a4ee12"
                            },
                            {
                                "filesize": 136823,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "b6bd31b93d374bf7b6af96204f6d8a62d9f938506a35504b748a953d152b64cad3926292b4e545a545e9833b903101e99459a3bf90aba432777ada44a020c04b"
                            },
                            {
                                "filesize": 39499381,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "72a0e0f7956a252bd09d4dbb3dafb956efae4dc285f254b2561b358e9093c5c5272a2fabc5a6bf6d0b990a53ef90291455b23d304eb34382a9cfb71b40e23a90"
                            },
                            {
                                "filesize": 26895970,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "e1d0b235caa039ef9518b91d5e6f3194c62bd1c8c89314dcb848ff5d542ebcbc1798a4013fe21e93d16b6d34a3ce86bfafce751821b9cf3698af5bffd77b1552"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "nl": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 80818612,
                                "from": "*",
                                "hashValue": "89f5d868899399b4ef5d94ab92973f1378d9612d87f1f8653b1a90fea0d8ef6119af34d189bef9aa3b7d829cf46e409d3313aa0e5821e886b8fadc2eaa5d48c8"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 39501744,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "e4492a7b655c9292495b8b1225861c6c1b28a53b7a73e0b078a480f583a5bd48f93bd74e268c7ddd9e20d5a741f893593dfb05a55d60d2dea153991cf5385eea"
                            },
                            {
                                "filesize": 136271,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "d0eb67cfe84a819526cd981be7575f60d4e1054ba574100346a401ad6f13019d2207a1e724d730d793027337bb1d9ddc0e707de4ba52c47b3cf720f6a3cf63e1"
                            },
                            {
                                "filesize": 44103576,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "5464a9aba28bfddb247eb4ec7313545b38d488044d19c787337e01fdcd346400f709b8ddeb0c6ca0ddff2f93c1ead9e84abe606922870cfaada1e5b31e09fa77"
                            },
                            {
                                "filesize": 26912782,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "bac075d5fa1ce1aa18ee88f5ae996893f5ab6f8ad20aaad94a9f598e12ab5a73ea84da95cfc43d10e92e57e411f69acf3f37c4174ae05f4adfd60a459fb16fc9"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "nn-NO": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 80050261,
                                "from": "*",
                                "hashValue": "c096b4dde6906a2afed700f902b7ab25ba1774e5764d0fe93a2609791761fb90fa2b7c10d5ebc306e06f4aebec1e1a86d05b5fc05107563fdac2e42d0a895b9f"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 26897148,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "ea0930ea319bbfc86a20e012000b3bdf5d14b661bde817d7ba0c64824c4efc45b20a8a1a6b462f6a5d7bca3eff62030fafe0f1b3b1a2cc88dd8376c951aaac00"
                            },
                            {
                                "filesize": 44103460,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "791a04c040a121590e020da412c95eb8430d0638e2fc1335abdb71ad9af3eec78dc32d3d5395819cba99e1ee6b67a3ee3de67d8b316da175adeab93c44862e9e"
                            },
                            {
                                "filesize": 39537317,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "bd6df6fd00b335745189f5d2131613297b005f81c2a30de9219ef5ae0394635e56355fcc951cb728d1a817948c4d3d39199fa45b1f0295233136b9139621804a"
                            },
                            {
                                "filesize": 136531,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "cbca159d8116e405646c0045caa6b03e427b04a0fe09cf864e28b3342496a68128e55798cb62c11e000c0289b9c01c9c78401c02ff9828f675287c565e1f16b6"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "or": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 80367465,
                                "from": "*",
                                "hashValue": "39d031539c1b203e16c43c9892b540270541beb9c5571ed66357c12096786b36991f7e23c85451d3c66b9c161de4ae3e568cc966f39ce7d79a47cef8ed2a0de5"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 26910390,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "05ecde3d1cdd0451963f2ee2f995edc7c7d0d6103b6ce0092252a8c0b33cca6ebf512f71c733a38d59c9dbc6d5e82e43a8a22faf76178853fe79acf6462eebc9"
                            },
                            {
                                "filesize": 44116340,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "db8aac5b0f496fe294cb457ffa22ac25b5bb145f7516cc36637f6125a0252f85ac0116a9c7113466c10d6e6488dcc4ad014d5f50a880b0085e38dc29e27b01c8"
                            },
                            {
                                "filesize": 39509896,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "b1f52fcb973e522c0889525e8ae903da221d24136610ddab1407fc449b5107f258929b1109951ab531f0e24683e59687a6e8fa9ebacace33afceac22d19a53d6"
                            },
                            {
                                "filesize": 132055,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "89f8c442783112994dc3155211978ab1c3c47abe15d1c9d41c57098820cdf0ee15f318a59880e61bed6b7db4b26be2934f44965610561d2c61cfe5a285f853eb"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "pa-IN": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 80108896,
                                "from": "*",
                                "hashValue": "d6d97a94e983b497648fce18d03e0b4593e100f80a39f9536b78ab1afeb203b8f53f2db310e5f5ceb7511b9664e4ce83f8c02ca19448edc5d9c404dc19a9e0fc"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 44099221,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "0dba6a1b6d612e4a6583d44647db03d9ac5cf9de53bf1e3246c07cc3669d4a537a6552715cd84adf22507f21d37142c008c2d40d0183e6160bc237e8c8d14ef3"
                            },
                            {
                                "filesize": 136156,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "8a5abf073a8c38a53006b7aef6de69d44b254db2b8b7620d84a52bf6e1b6508efe88ca3b679a324e1d6da77db9311de2b17d85fce5787660e6cc353beefe7a15"
                            },
                            {
                                "filesize": 39502331,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "ef82e2824d723ce35c8f9eafe30bfe06ef884b91f2fb010a1d541e7fa2cc24d68b863a8a9573d418301328a8afdb6d3fcb434dab323f51a1eae3cd5b5796b431"
                            },
                            {
                                "filesize": 26906180,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "e617cf69932ecdc6e889bf42760d70ab37b2f599c6f84680d880259aae50d50bd4b62043c401b823a87ae2a4d357f1667e263917aa0d74ada2a8307862ff5ced"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "pl": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 81128995,
                                "from": "*",
                                "hashValue": "246a8c4c55960ad954ebff82bca43971dc264380f58b5dd7ac3b60e99518da3dc81212559a2dca485bda19386c5fb8a36941b64a2d7f172034deba5e938cb9f7"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 134569,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "3e6cadc612363bfe925fc33b08f95113f7b5285d7c645db04a9f5da1b18a22e1773f4718802847fb7ca31838b32c1514f6605104dceb45f09775b6f816ea4911"
                            },
                            {
                                "filesize": 39479342,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "1c7e11696033ec3f0d1ff011f73f167b0b43c30e4505d3d512dcf34a4257438b467f58748aafdf40736234da0d035fb75e7488faa41959082478a9dbff98b91d"
                            },
                            {
                                "filesize": 26875955,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "cb1338584b459ba4b7e00b92522baa888111196c5a6c24883bb2796a049508a3ddbe39b87294486352a7bcb5b0ef23356c7bd04924a9f5a53671551850bc61a5"
                            },
                            {
                                "filesize": 44067410,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "8d391bb5390689cc3ecf333393f431604d131badf45f94ac5188a615cc8f958a0ca93adc4a4c57dd2f4d28310c7d2ae5fd3fcd4bdec02802cce072d7e0c8196e"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "pt-BR": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 80249470,
                                "from": "*",
                                "hashValue": "ed69ffa6294a7abe0dbe8dcfaab6ffab6c782c3df3ff861029b1b89ecea1205ee12803e5715648bee122eb61871bda9f4b63011a631f3aaaec36785e2f847921"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 138220,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "a12149e25825f9215da25a83bce4d21a12f61a2cad7aaa4ac6cf472d35b8c8c8be49cc491c8bb981ef893f663aff5b797e224841eb19796c6b8e277aded054fa"
                            },
                            {
                                "filesize": 39517878,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "417e70652ef6c2b43794173f54da9d62732e16ce76de2d8696e2a444dd1b154c5c12a629290bd0093c81ac9b11387ded158446e3990c6d0810c4cb2fa4df7cf2"
                            },
                            {
                                "filesize": 44176638,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "08811a5949cd6309d1d312a1cf91e4fef26a70d8feb4a93a02f01127315c87acdcc053425de6484ab4c0a18f516bbcd7d27405ea1e3430cc49aedf739bd62c17"
                            },
                            {
                                "filesize": 26892894,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "9273b4766b598d5b48b706489a79711083402613b9b1fcee857acda6d2eb6e2e474ca6326c363c54bb4862bd69dd0d2d074018d99c7546bc142585cfd96ddc50"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "pt-PT": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 80239873,
                                "from": "*",
                                "hashValue": "e0fe96df1b2830e38ca6e86a5a17c77b2b21b13e6cb6474ef92ecce7c9ba3fae569c3a9fbca95af0bfd5cbcf2e201b904206c2a83e94899907012618acd3d577"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 138454,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "cf6004ebf9f3b7354c6dc51f0323178bb5c13c213065af8d218599f8e3cb36f27d4086456c1483c089e7fb44583a1118550b3713ffbbbaee05049dd7f4e1b2e0"
                            },
                            {
                                "filesize": 26983703,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "72d308de685719e658913946bb6c76fe1711f2306cfd596eb83a046a121ba5d26bef5dfa8cdfaccabd8620acbaef41495bcfb4b584eb520de514724cc2ab67a2"
                            },
                            {
                                "filesize": 44220099,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "7adb0c2421d06d6f2260308754d837b81411b163912598e9be4b79b79a319d48d6aedff819144ac0c3fb822b500c06036786ee838e37dafbbfe12c1acf4d68f5"
                            },
                            {
                                "filesize": 39603124,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "56d26be75103a2b459eeb19bad17cbcf3491f2d933fea8f6cd057962bb541e2d2f4523fe2a34fb8640179360d8a5c3a8e672bbd006d1fda52e0ed1360dedcbd3"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "rm": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 80056170,
                                "from": "*",
                                "hashValue": "2f1042d7336430384eaaccadbe57372d57ce2822435150b1efde363d99ec31100b5de6f4073979782329fad1467e7f35d15a789c2c3d597e97d1e44cbf8669b2"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 39605542,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "636108af1792735adb5ab8fd96b38f91857143f79dce2900fb873caff448087f9a2b40f8b3e1b023d67168a75ecea03b45b6a931da2c97f9f2525456b4f31751"
                            },
                            {
                                "filesize": 135245,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "82157be5475ee90bdefd952ef211c63dbfb1a612484df75942f8df95c24124c1c4d4a0d257ebaac72a7d93a8174fd31c00b2032b34b7070ae54364d3c3eac8ec"
                            },
                            {
                                "filesize": 44165980,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "3c318636409ad327b3c4d395bd1f02b36378dc71038b4acf52ee5fcce79cc427b4f7343d92c58f6582f2712db8267c2d3019d09e4a4b3673dfa3097c3b5cb042"
                            },
                            {
                                "filesize": 26892181,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "c4a7775ae74391ec0656fea55ba5ba3147834599d2f09cb3c0da4c6dbd9a38c537a93c7db63ba6742e51804ae686021e86f6baf21d8cdac30794acebeb35a36c"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "ro": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 80740988,
                                "from": "*",
                                "hashValue": "d235a6c959627dcde048f1853858d1390ad8cdc537fcd39d7aec0b136de7ae74ea713ebcedb91c3b4c59b2e8b991fe03805c60f7acc33420f63ba401ab03816b"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 26919589,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "c6ae65d6f8498328807ed57dc0be3076cd6ce0765e95d28c044bae30a6d333b368914b0bca14900e7e2f3d81f206603e39ebddf7ce71461bbca3980838ec2414"
                            },
                            {
                                "filesize": 134653,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "f521acf37d5db195ac993319715801e1a7ea756f525b74fe22cc8643d1b358815758ccdbb6e5c7e889cadf155aa1c3f5e9fc8d9fb250d5aa4ddf9b65ff660b3a"
                            },
                            {
                                "filesize": 44240454,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "e59b378662feceec437ae842035b49e261e999a736fa72b4ae411979260f1e0dd78b443542796fd9be4c02d35614d7ebe31bf9c5a1093b16d6504488a3b64597"
                            },
                            {
                                "filesize": 39667436,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "b4680d7feae7de866eb2016f1d1672c9c93bdcf81237746f2fb69b8947fa6a45abdb910f25af2dc62a77589e0c81c6ae87e7cbf24aa0f9ae352d078cb508297f"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "ru": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 80544013,
                                "from": "*",
                                "hashValue": "514fa9ef9ca34f29946ca2395b1df89c26d7e65cc89f11767a5822c33f902cbb45cd99fa05e2c911c4a9a93f84ef2f71758f4a66b83a1f29678f02800550af9b"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 26879989,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "c3c4a8e61c61606edbbc176c592f4d3587dd3e8c94d32db8f5f10e25e5835a49131976b28a441e260754de6f88296b50179037fa055acc1eed881383c739b094"
                            },
                            {
                                "filesize": 39476005,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "4cc2aa42a77316f145d29285e34b703b8573808a87ab4122f55f8cd3dbc7c6b0284871d5c46a980a7e7af3571ed7e895ba9a6035d7b5bcaedf3a19e256212409"
                            },
                            {
                                "filesize": 44062306,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "b32e884155234806c130a3372ccb7cfd3c8fb8876239d6b48c742abbcccfc1e08f05c6eb0e1953d5ca28c0ab8fe9b3bd09e00bd88c217f7d4ee4827c984655d3"
                            },
                            {
                                "filesize": 136247,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "25970763d3b1f2eb011ccada6979b0dba72e25c81fb95ac016d8fa35d6b7a2bca62dfdafb3452fce2d3e54615d9dcbad4beca3cec1db3b0995a2fd80be3a7ae5"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "si": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 80150290,
                                "from": "*",
                                "hashValue": "cb5201b3cb528270bb17bf729eeb72e22e2bf9c0c99d8d4f9f9bdfb00586fe97c06e0158f8fc2c058e8035e0ec0e5120779113b847864f5e9028be6b67f28bed"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 26913195,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "1a478d151e31c5e41d3f2c67e43e0d49d4312841eeeef60eaf7bb917350dd0c4884456a1926525e229f8568fa26c1ea2d4f37f3c882047ecd508e3f08a39dc5f"
                            },
                            {
                                "filesize": 39674277,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "d68979b4cadf9a21275e2424d770877353930a35b5488a3b90d9f3d1276157418d9b96ae803d661560062b73a5fd3d2a08f1978e520e3a2cdcafb6905f144020"
                            },
                            {
                                "filesize": 44248824,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "3d0f26cb63fb80b4b7f96ad5b72db638ae07ea7aa0905bacacd3a7c179bbde88634030847f07dab014e39f1b90c777fce1c023b070838548e1f7f2ee248b58a0"
                            },
                            {
                                "filesize": 133823,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "cb1da4c425996126474ec3bfca74f4c03a6a1a44225c4e8f9a0df44032aa965ea14a0a4d25c50800fc765b807bba6052ad9e0bcafcd2beefef7fc77580e5da8b"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "sk": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 80979997,
                                "from": "*",
                                "hashValue": "008e8a0740afcffa5defc170d536adb648866255d77bddc26fe2f4cc967715a8ad03c1e1a6a5a8d31cd56ed176648e1aeb1cb5cde9962496414b4f4eac0f49d3"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 39499326,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "edc440f1c4e14d32484da0323e2b3e26e4a0a49e25ec4b5e88c389396c46e6a40b97009fe621c3ef25639401fd8064890e5aaafeb4ba50358949a1fdbef544a6"
                            },
                            {
                                "filesize": 135032,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "68e6364051b99f3eecc0844e1d0c4b9ff15b6823b2aaed6554d446744a387c2b85f2edcf7432614cad22156bec54b0a02d0b1267b98cbd9eb798813844891cf8"
                            },
                            {
                                "filesize": 44103945,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "45da938b76d72720aa8e74cd9dd90a05e880c22085fcca79e54e83dfa23d5a86b199f0c0902a2a4f3841609919505b2dd50d2a3d966a487481b8b8a48ed6580a"
                            },
                            {
                                "filesize": 26911881,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "a5ad0b19be1a50a550bbd2323b071116f1b2464af0afcd83fce16c1cc25080f8398145461656abd6e8dfec8c907a07285ed85ba1717403112807c5ac405dded4"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "sl": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 80054116,
                                "from": "*",
                                "hashValue": "9aa9d8adb02ab85711bf64d8471d4069500abf6be752edded18af5295993b19ba712ca918c31672cd980486969aa8d680810612ae8c3d62a347b3133dc2d5b9a"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 131930,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "d7f94136faa4b721fa4a19eda06ebc6a07a60741265484b65a6d3d847ff72a335f02c5754627ddb271c4964dd33ef5f71752d96632315189a9e704f7887c9935"
                            },
                            {
                                "filesize": 26903598,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "3a8bb4654504d8cfa885adda75d774d6beec8712b6a2eb5cdaf313722a4161a5e4f317ae0ac53109fdec86258929c7ac5c36dfa44f52ab7f977fb83f2ac8d3ea"
                            },
                            {
                                "filesize": 44102927,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "26dbc68011a6e2e2783a8bdb413dbf07ead86aeec6d7a13301cd8478765b96661e7937f4a4873402f9bfff7183e8684c0a40386856ee97c56d6430e97fb0d1ba"
                            },
                            {
                                "filesize": 39513411,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "4b2f7750a53be0e573dcb4fe9dab64a43f0ffd382a23a4a451fe911bd62be8dab655247c4598afb7a240d10450e3d145152952e3176e124e323f31f1fdff5919"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "son": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 80061723,
                                "from": "*",
                                "hashValue": "6519e9612f13be75216d99a6cf73f0ba829e4a7265487b6317258570c0564364bce1371f3a9ed151c6283b58518e7695da0f98ce8ddb75f309154bbb1110c0f0"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 134335,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "8554df2c370d3f62d958518861dd898dda728efa1aa73455831612d7706915a140681dd584dd6e9ffdb6dc96481741cd7be8a4ee810682fb159dd6e8e021aadb"
                            },
                            {
                                "filesize": 26894185,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "d8e198c4452c941b3d0d07dc9883877f7355bd1f9bce3cae1cd49f1b954613a31b22ef7655ba22a98b7b07d8c42de48537404a395f0c631e9abcb5c7ee5bc3f0"
                            },
                            {
                                "filesize": 44138284,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "111b64b0ba59dae64161b3daaa7da2c3d078311ce75d3a293733a85da8fde458e82c7dddbe46e30765344b9dc570115d78f1979e37f64437419012096f673d13"
                            },
                            {
                                "filesize": 39544720,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "a6f5233c086bc08bc1a7889c4de1d2ef2c5f69f5a847eb540ae40a56043be9e30126a4c2d48f84faf52c87feb91fee5b8c73a86bbb1cca8e338289dbf3f31012"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "sq": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 80097283,
                                "from": "*",
                                "hashValue": "9249d1855f8cf308d4d7551ebb31a204d846fa8875ce2fcf4fc60fb3c83373c706a5aebe12ee78bc3afc9e24f457deef7ecafe873c412926a676adb05fb82721"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 44139804,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "0647504c5e9e3f280a3e87059d7f5122636aa5b9e3724d3509e45c1440da2eee3e324eaa1b21259b73f1ff06fe00d976a231490113e9de26959b2225ea020f72"
                            },
                            {
                                "filesize": 136812,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "29d525d8af91f0937a4dacb6e6e4bf7015e3e9af4e0a41c3916c3a894600220bdf503453705ad2ba6b2ea895d7b68f3dd4cbf02fec22004664b3fb3dbbf3effe"
                            },
                            {
                                "filesize": 39568417,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "3ef79b528d975f1669e6f57b03b285fb0e4745c59338bd1c707066146aa7aa6085b3762f27c29030254f189e37b582c449567ee2f1cc4d0f0f6aeb279be7578e"
                            },
                            {
                                "filesize": 26910683,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "8d88dc379b78630960c013872c193cfc4201a081b837aadc158b1e9f90a106801f1f570274abc4e62f66251957dbbc4d947f56a7f158acbb147b7895660c580b"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "sr": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 81992404,
                                "from": "*",
                                "hashValue": "c8e6e897b4b780be639c0b7f4870cee01d2fd4303572fb8f8e168e5da54a9b64d59cbaa42c4a322535ae887541c6530957827fe94d7ce3080c7f409574157d0c"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 26907200,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "e47ee0aea4af6b9255f8c3ce8daa06178e5bae821b3e52fa8f3363eb2c201c1bb3cad1d7e3d7c7e6234c56a3e85f03be04d840dcd77bd330bbabc0cd0ea0cd60"
                            },
                            {
                                "filesize": 39621124,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "73c1bad4e7686ab44fa551ee3e55df83165140b6e85c80bc7d56dbbed5491c6f127f926953c5eb4a2abcb159e0e80ccc9a88c04c7017917e2e0551aea378252e"
                            },
                            {
                                "filesize": 139922,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "8545a0ba14cf1b9446bd5336bbc3ac76a6455510ac7b6e6ec3578b9990b959a00c69352f050ee0792e71d3a3123f92f8e4d5af32cba21aa81c30a57075899135"
                            },
                            {
                                "filesize": 44204895,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "2f7c345a2a1fb80675927a2f09cf0ac8364efae9f6feb04f92cb43c95a9acb20a9df6a009ede214b819b5dc278c937e2cd63eeaf12067f5d6886bff82b352e8e"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "sv-SE": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 80687248,
                                "from": "*",
                                "hashValue": "2a0cf4d836b1e6143fdea9d54e05ef24009df03c4ba77e2d9c4b4022b97969d3dff8b15a01b3ea76077107d957101061c5edcbfb22e4061fe979e91bb9d34708"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 39517740,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "3848482c304be2cbc7cdd67da3fb81bc2be710c0e7b25312055119a13818180c5845f12a7f44d11e34b01fa12f99d10b1148ea2995dd0343a9a4d430ecf7da2c"
                            },
                            {
                                "filesize": 134880,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "3769e8a2b00e08b2fc6ff942b06152a651d1e1e860f1f9ae6461b6c82028bb7aa03216302ca81769060a842ab3eca80430ee8b3e6c7a56ff65f17c816d913ea1"
                            },
                            {
                                "filesize": 44106475,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "95181ecfeb66c8b4d6dc9af8919af25500ed1e89bf127b3b3c55bbbbd4f69c393db367696d5637b86bbc9b8ad4f36c17209169ed08c05bd8a76fae95c9780fd5"
                            },
                            {
                                "filesize": 26889623,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "967d0bcdf88de7b9326129be4f20d0632ee1ca90b9c223ef675eaac2919ba9ec29973d31c58fe5646e1f67e4c543453e4b2e9fab433660ad2a9d28fdbf58e255"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "ta": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 80377016,
                                "from": "*",
                                "hashValue": "fad812ea48562012e8cf6a83b0002d805e2efed3fae5ee6a26e7be1ce81d04c636db48a929f3a9577f209ee9d2ebc80f8aa7fe62e1c5f37aa3e7766cea91a67a"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 44117833,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "a338aec3a5920e3e09593bb6d8fa912e9d4278bfa5ffa84ad9f5279ba7228944ff75923e5670d6c9bb6e145720cca0938d4ad30e66c30d772c3f0c33bc4404f8"
                            },
                            {
                                "filesize": 133513,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "802b7ecbba9f4acb43832bb6901fb1b06e8e17fcc267f72d254709da4e7f60db8780b51257ebff1e1a8c78db1eca2eb55e73308da3a4459b5feea0b28bcce268"
                            },
                            {
                                "filesize": 39507291,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "322fe887d0e46b3efe1fd61646e76272b1d598a22d86272cd68176bf58dc194855377bea770e9140e7abd117c051b68b7aac719f9ef87736d2cca86f4f8452e9"
                            },
                            {
                                "filesize": 26901859,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "f32e3415a71efed7c0581664ef916232026d13c6a530bca936de85a00c3d5898ff1b11218ffd502ba4f3d8dad78dbf8fd6dec28acdca29d7ed29f4ee4d6e3174"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "te": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 80138292,
                                "from": "*",
                                "hashValue": "c16d7e8276d60829f98c87b3bf521350251acf6a185f1dc23c4ab2d1fe4a1e9da8876fb1a086fe26e220f0c16da2acdd1fb54c1e7b648cc2d00adf6d0d417ca7"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 26889305,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "b3e35c79d6804803acd0265149e28b256900481b2ce76b8b2139e15a5027ce4ae86415d9692cc2ccb82a15ac44e2c8579a84c066a576b3fe09733abbd21c0806"
                            },
                            {
                                "filesize": 132597,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "581a90076d522a5bdd434aa909d218fdf593ce5e39d2be5d06bdc8c575869526b3c539bf35324d17fd831d215d21e6f6856cf1379aa953170bb50263948680e8"
                            },
                            {
                                "filesize": 44184296,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "67198c81fe2b1da0ad69d2d5b047b0d6a9c761db67c1fb437e3d24bf432610feddff487d7b305d231c17057b6c650c88e77f55bc45d1c7ea091f33e224adb90c"
                            },
                            {
                                "filesize": 39622996,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "71404582ffa76dfc6cae7a8bbcf4c58500a0909a5a7559772f1940a6029d32fcdf41ad6ab4c043337845ac160bad5772849d7f61dce7d4c063eba0b70e147b06"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "th": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 80148588,
                                "from": "*",
                                "hashValue": "6f44db641ae154467bbf73ac9c6f5654553ae7245b7e10ca53388a887fab905bdccd0afbcf389854fd2af386a0931806a0138c315757759ee9a1ac78eb353938"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 39615481,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "1ae1a868b51f4b4581bdc1b44778dc2c84ec00c00f0e7244ae053ee71fd17752d417529c8c709684c23202695b3de1bd3087d160a87fba37bdc2831e249cd417"
                            },
                            {
                                "filesize": 26905575,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "5b3bbd5660ea6c4d3f1b14a0f34032848632c16b6df2852f0a001000b53f582773d6051e2c4426f26c792d1ccf7b9b103672b70f75762be5ac7671fc7fe20912"
                            },
                            {
                                "filesize": 44182536,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "e510348bb6ad9d9e30dc37af3767d186c75772a95577407aa1ef8997d4c93c9124a1e331d25c26f7f45c801f4edaee2472ba6ff37e8a0bbbb52063f9b4627939"
                            },
                            {
                                "filesize": 131916,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "ad74ebc793cc8bcf2d6097a439837887135578dd1329d374c8fb0230468fab4f1ba28f1c52c8ac6ce95f0c14bf310c76571a884e85e22c326cfe426298f15de0"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "tr": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 80095536,
                                "from": "*",
                                "hashValue": "755f75835d724b88b192c34500f66a2e313030d1cb20ad02382ae22aab07905278e3691d765d2c798ad81308e601cd91ae2d1b3d5abdace68a2d99a4985af429"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 133481,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "2acdcf538cff1aea4efc7be2164756cdf92d2962a4b58144796810e8cd7043e8fabc0cd2debafc65c4977788e62a2876f452c60a83ff415209067b4d1680af85"
                            },
                            {
                                "filesize": 26929586,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "5e93884332c40d895b139c56121461f87ea1172c01aec0ed96bef25b7827da1d9c076aced54677a09e057763f1d7fb4f331564986143d4ccc979df07a9024ec5"
                            },
                            {
                                "filesize": 39561889,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "7d8abafd6d9b77f109404cf79bf208480821b4b62edd5091bbcc4d85fd1a2db228c394b36e5174a773b0257018a050452c10153adbf266c91a84d710c78d8457"
                            },
                            {
                                "filesize": 44151440,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "3382a5c81e64afc5a0225ac15e4e930132a7bf2d21f566fbaf3a40fb37af9875fff20db64d6802d4aa3e948dfcab105f3bf2ce8de25f8f4e76b4b7284df7d492"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "uk": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 80537264,
                                "from": "*",
                                "hashValue": "e3533239b9ef03fd4fb8f53473937a30ae9b21f02356fb6c81a5614ee4f6a2eb780cd758aa79acbbe1ad02b0fc62d7662bd11316c88decf1291bafde33d536f0"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 135752,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "49e9c236f777de51969de671b8dc7c13dcdb1d2901661ff560a7f495848860797a76308b0914cf4dfc9ea760889b6895c1551d1ac7e994dd2c7285d9ad28bf53"
                            },
                            {
                                "filesize": 39539861,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "5aed311709697d1e8d7e764cbffb22fb804f317b33cf9f61d10b2180b428728f19a07cc8bced9b36e822038c44aa6a2c2f3ee848872005d90b5dfcb174c919ec"
                            },
                            {
                                "filesize": 44159552,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "9b11c6cffe77d615cede73f383a54079f3ed31b260aea8c39396a47c60102d20d49f9338af6c575c78c283d6f279d07147cdc2bbffef46f84ada4af4befb2be1"
                            },
                            {
                                "filesize": 26933695,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "4de4c6d097868494dc05b0fb47246eecc3e70359fc24887548412c34824b4541e9322b814ffd7f36b856b8776894fefbc024c3c6ce28bcbc17b557c872edd450"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "uz": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 80112964,
                                "from": "*",
                                "hashValue": "86a11ec596d54ca0bb9d1e4b4db8a0f25f726c9008d48bcc76a4ac25f66579249ce66a4dcd809b205d8316941185c3b980d82644027a1f13b3f15c7bec6c6ea9"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 39585285,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "63949a60d433c200ab8d9c74cd7a22b12057a92b6a3be5d8432a48e57fc77fec178d1a3cbdfd63b6f7ab37a6044fd4c3202986f40466fcf265acd64d6b546f23"
                            },
                            {
                                "filesize": 26879896,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "74f44d1dfecbcd8c71128491f7f15885e1c8a18b6bc60fd1dce31e1354ddf821f831dd867a4b35c96b9766d0886df690452133d3dce404bcd2f16ddc877bbe3f"
                            },
                            {
                                "filesize": 44156710,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "fa5842498f17e3c0e04a5224756cccf8fa2eed81055aa5f6dd4f0c86a722003387f3dc854cdcb218862e831ebe343b9f9225a26c4afb018c51b71c97be94764a"
                            },
                            {
                                "filesize": 136131,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "7806425106c9c9c53dc62c71c30ca36f86164c031657df1506a35048d363d2ca0b48b6cf6777dec072a2d760f444cd19c7b0fc7c5b96122b9a260ef9ed3249cb"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "vi": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 80108552,
                                "from": "*",
                                "hashValue": "671e96dab10b1d963b51cd0831f0ecbc902d616fd80143af261da9ca78f3d643ee25fb4ef5fbda2a56a9cef009e041cb3fbfd648b5cebbe7759a5799158642d5"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 39593563,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "86210ec630939484cf8ff793715693ee5bc8fb9e66a1662f3fdf02fc97fe06655aa83443b0da0a5345b1317b8b338116b1e79f7326fb86e147f4de6f1f633ffe"
                            },
                            {
                                "filesize": 137903,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "f79bb212c36ac4cd9f821a4706447148e3163fc46cfe469c58dd0173225c260e7f458e56237917b63369bafab945ec7e7d91b4425f0cb459d0598d1c2eb20bae"
                            },
                            {
                                "filesize": 26900264,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "5bb7cd8260c9f635952b5b3b5ae53c1fb3638a64e7d69ac2b79d4b7b880d20ab124aa97588c320b002032f764d997ad3cf5e29da8770755e395a67339ea82609"
                            },
                            {
                                "filesize": 44153674,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "fc7d660a039dec65a7799327a2343ddbdaecb65562f912095ea10007f86e1f6e3d5c0e94348619a8473afeeaca1325f967be740ed61aad7ff3906112d96714c1"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "xh": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 80057687,
                                "from": "*",
                                "hashValue": "7b6d7ee90c1c79e49900bb8c455409f5a620903f6045a1e5f7fc6542081274e187b99cfa07b9ac51494979aa76e44881c618120ce2caa974b9991dae83305dd7"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 135537,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "536e31ad780ed19436a5115bac1d4bcab74053759e0085c857b297d2d451ad12dc6c4a08361b3c65b1453d585552753bd44eb2c1978f1524003344193ae46d8d"
                            },
                            {
                                "filesize": 39635045,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "8e807b653bdee19cb32e7241be643d2a5a0ed9d346780d1b824f103d960b04ac01daa4e135fcc98159ff4607b60a54296357678ecbfc1a37f87df8ee15b6527c"
                            },
                            {
                                "filesize": 44195679,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "23bc31e6c17c94f7b902212e66e693be0b3d0cdf163b86bffd6a0d809f2764f60bc272f8ae013ca5ba98559e0b30ed62125c04dc60dcdf4d2949bd28338c891a"
                            },
                            {
                                "filesize": 26947051,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "f51e4e26881e2fb5b888064e77a436e3c00f2366e093f5a80b6aa934411a8d8d39dfc5b1c4f019d514f66b0cc2438553c7f7da7ac4240010c41ee56ce32ea48f"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "zh-CN": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 80091961,
                                "from": "*",
                                "hashValue": "302efe3ffe4c5b8af4be495029d1961e6139e263ea43b37ab6ce9e4a99e6772a1f3562431d5f117cd10d3519b9f821a25a9985f3e14842fe0f6c771b8928cb78"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 39520022,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "91de9fa98bdfe8cf53bd2c85d71d80c13c6655f02e46de620efcc5dafb9687017baee6cd5b022a213b66077af66f355970b87ab58c0594a9136ab750ba775a72"
                            },
                            {
                                "filesize": 133761,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "03469aebb0c7be4b66b347a7d061d12162a4d1b68d1e55c1d75ebbbdd2fb1c9b473dd9b37c55be75ad5002e2e8d6a339ac5fb34a8af14f0ca3f71e6888f30311"
                            },
                            {
                                "filesize": 44113912,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "6c28fac2dccc3ade8b02d823d8a21079484cf9e423e71afc9eaa3e1ac61fde995c2ae1f68618695fb7f306827afd8701de6876647c5486cef84cd53d1203edb1"
                            },
                            {
                                "filesize": 26916684,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "2a1ff83c1fd051d57e1bf07489b6d04337e2cce4ed768b32a2152c0654c290d2e308b9c40c9ee07d2e01a36113ce95f7706b66c0108dc55c0213e1313e9ee09c"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "zh-TW": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 80314623,
                                "from": "*",
                                "hashValue": "1f88cb4725f8c3a7242c8aaf672b20edb8524c89d9d1c882d0b0cfff865795ada142129b73732d9c7da1946465ce187dcd5233d0a4571f6bc9187876bcf89e78"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 44130318,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "bb37f93dbb81a7ee13c1fa5a9174432d4f6ec9547fdab9388b5415dd56ae1738368d45837f809680cf7cca61973291b061dddbb01552dda77cc93648c7f6a417"
                            },
                            {
                                "filesize": 26945240,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "421966f59fb6811c9d70cf0074ad6166d66f3a238b557af941947050d5bfd7a77b23e3d3f4d28a1bc60cdbd740d1421e89d55fa539e278f8b9862d2ca154ae36"
                            },
                            {
                                "filesize": 39541769,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "a81ffaf84425c3968a21ad642222b0651d64cb3bdfa0204274ca93c44c94e0704a6d1068b4b0eb3642983fabdad543e7cf3b91e82f2c3a48cd7037f0083552a7"
                            },
                            {
                                "filesize": 132769,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "02c5834ea5a79bc7ea51a594c6b20e5edcf013c095ece4146b6e5e0019528782cbe75f6c7cbb7eb4e8f6b977c88176569067e9693d30a5161a4a31919c3bd8fc"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    }
                }
            },
            "Linux_x86-gcc3": {
                "OS_BOUNCER": "linux",
                "OS_FTP": "linux-i686",
                "locales": {
                    "ach": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53222826,
                                "from": "*",
                                "hashValue": "44963a8a53d4cf9e77044d2bc15dbb2dfa59b376d4634cb9b35bb36e29160d35efd7d2b345420e533f6843bcfc2f28e58ab0c36e150ed5b6423732cf17e88db2"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 31352177,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "331a32bdaece6d75d72b6daca5555d5f9bd324740687f563ef348e54c084d5679f2159d66a7df3a0cf478aa6a181527e4da06d368d260676e9c85549f835152b"
                            },
                            {
                                "filesize": 22820627,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "413571599149d115b67c54934b0ae82d8774285c2f02624626bbb6fd77d34d7f8c92fb550b3a9325cd67ff9de26c61fadc24bfc3af763eade0420a1f9ceebcb3"
                            },
                            {
                                "filesize": 3438467,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "22b0dcd3c8710eb151d6dfdedaa2eed6b80b43e44b17188fc394ccd2fbf600381438ee205ea27420cf1a488e6a013565ba158f7886e39616f87c3faf0fdc484c"
                            },
                            {
                                "filesize": 28935173,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "0f1a9c4ae7c18502db9a65ab65188e4d00ffb79053206aa7c84477a0f15baae32b1cd38be989d8e9527c3fe0d4f4b87485fc98d761afdda91a83115503942fb6"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "af": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53232244,
                                "from": "*",
                                "hashValue": "ea05eff6cedd4738f26aab059f22b7657b6ead2e49ea18a1ce8b01ff263c06d05136b34c48ce985b5ffcba2ddd578053e39f8f64aa0caeaf52fffda126c2c4af"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 22771359,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "2d043d94ad2fd9524800989047b25d7b4124d697be27eea23c360fa6d1a8b9d1f55f1074e7c88a69ee3824dbb3ef43565766ca3408c8404e784d101881cfecac"
                            },
                            {
                                "filesize": 28873328,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "af525b9ccf9634697b50a58ba5798e319ad13e3509c493d5d8af31b6b643230c1f07f349899997d477d5eacae81c481b5c77a00fc82ccfbe23921f85dcacafd4"
                            },
                            {
                                "filesize": 3438412,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "ab4c15aa130f198afa36934faf25d3384d04563b2a97f8c7cdc13349059062c83d061f75e4a468cc2a62e5826cbfa2d0c6afd96a6c2274bda81dea72da6d5c72"
                            },
                            {
                                "filesize": 31326417,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "7037904a76a5b81b4676dbe8404c56661bc9bc57319f93b92d88e8c287cc9d33c148fb16a181507755f93db720f23a8fa629b1f2cf66a3eda25204c9c07d981e"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "an": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53209981,
                                "from": "*",
                                "hashValue": "0b4964b16f7366da63b5e52cdce1c1666c9cedbb2eae0817c594911c52fc042840362587cbbbe835e311170f3bbe8bca06f5f0af585f6d4f7d84e72aa86c7f89"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 28851298,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "80b646eab4310dd9f25f0f7a253e80df1d1357ddca7c78d5947f5e4d6affa753d729f6f7bc5c8c32b2b30b9dbd91cec7723075112f60d91edaa7987c25694cb1"
                            },
                            {
                                "filesize": 3438430,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "76ad5f322f319b24d0465548af136a9232097f6eddc17467e9b1fb6027ac1880f066c2800dc757313ec6c1ad638148cf91722d1e15c93b73d0113c3b82e550ca"
                            },
                            {
                                "filesize": 31287680,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "e5e3eb700ea8c97a51b3ed171a80764c88322a13274eb9450287674e1b3486cc7656d375081b54b4d8f17b3591326dfa08787168aa86a793842bc3022eb5cb2a"
                            },
                            {
                                "filesize": 22771479,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "9b7e34b185a4a96a4b32722e515aa95603db7cda4051e0c13298ff246c39c84817111b7e3f7edfd0df0c2be47074636a2e469699890d3d7b54f1647f3b2e4a63"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "ar": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53269526,
                                "from": "*",
                                "hashValue": "adcb9bfe615531e82283789048ee441cfe3c396dbf1644ce0af8d886482a597be9e30f034f5e95ae9f4c6710742b1fc46fe1b40497b7f2937877005eb4dc0d88"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 3438741,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "4bea6aaea471e9428b5d3c66a290bac65d7b3d8ee737e4004ead4f6dba859406c3018b57221b230a12a766d726dfa6f09f227327647afb6cf813d8cb42a76f11"
                            },
                            {
                                "filesize": 22765353,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "7ce60d14194d4cafcf66ff099dc762a719cfe5314fc6591ac3da87721bfd8c4aa3789d90d60d4e3d937c9c18eb439b0970a96d8953c3045abc0de6dd7c1c9056"
                            },
                            {
                                "filesize": 28903623,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "308b4d02f42e3d00804133c63eb4e262ce889e563c6b676a1ec409c240b11b9d81fd4a447e6f58f5f3d45fe99056f574aa961dbdf0249b2da906bcefd60ec2ba"
                            },
                            {
                                "filesize": 31358712,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "46a8b538bd0690188887e1ffa9ea90be1da450fd1a0e48f84e73f120353b463254f821b10daed657da403eec61aeb843e412edb7647542fb422dc151b3670887"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "as": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53259752,
                                "from": "*",
                                "hashValue": "579705f37a3af2b415d8770d1d3e9ed5f9e6807b71fb2c54c1e7f68379537495af96bcbcce0b30fda0d15c23267e5e5738b801abc767c699ca3dc77862dbf1d3"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 22778655,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "3b0916b6a56e73b49104ed17a71e79024957c4c7c8c93de6f2427946a76c664bff1bb7e669f23b081d6192241b1c9abc263a3aa86538fecad89d042f5fa74934"
                            },
                            {
                                "filesize": 31302219,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "044eaf4df1fd4bbdf0cd8f47072b7a4d088d4e60ed1a20b0a856b4362c2201cb539c8b7589184137f64a37d561d33d9f3b00419f3f8c88d0029a7b3d3d7fa34b"
                            },
                            {
                                "filesize": 3438672,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "2f116036d1de55de4df7b5c1f082e3fd826db7c5f15752dba8b25ebf53024e15df1dd343fafe591277ff47309a7631e18ece71545a8e2c4078b022d04762f41d"
                            },
                            {
                                "filesize": 28857117,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "b02d0fb1a81e287ce786e9d9ff8d6a27eef9d4f085fd593206cd2c50e885d54682bdb9410d6da72511d172595ff79541fe1bf46bb349f8eef15003c7e5e23f58"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "ast": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53146911,
                                "from": "*",
                                "hashValue": "1170fdb29237c78e635a0d0de53fc34e906d25162b5feef7bc68a40b1e249d5f7db249b0a89cc113d846bb81c4c78cca3e890696aa2a4efb5a8cc3e4afdc2353"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 3438677,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "0d9c66f78f967f8e12aa94337b27d54fa37cda37acc484d5943cfe19235070506542356419f16e5a537f9f36dd907368be67cdbce95e4f556982b19aa25f0cb4"
                            },
                            {
                                "filesize": 22749870,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "32971d02e85e2317d0176d0d845de1f0a5fac43c268aa81909771e13abddb56b7e05a705f9c4c28747ece6e7599fb645a2d83a917a886d9e49dded8366d8d7df"
                            },
                            {
                                "filesize": 31238998,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "6a320ceb793ac15fb75115cf71b0c978ee7e0f8a47c1c7d45f67723938c5a0f0dca19715f3cc667ad517f49753f35f41ada6a046f30071013c9601c334be3d86"
                            },
                            {
                                "filesize": 28805175,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "29a6029073b76f3c337497aaa2de4b312c3b3bff9c1df916e8e07150e8e2c57b55a07421c5f2ed3a38313e22f077bd0125427560cc7cd1a0b437c79c6594e3ef"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "az": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53241233,
                                "from": "*",
                                "hashValue": "622982ee66df66cbf440599e1655b57acd84e0c85f82192f04399b2c219da94085711fe903d692f2a8fec385ae71ba6434e5c5d03f3294be7ce9e2048c716187"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 22821693,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "37dbd02b806b73b6e892897e18722c3f68b944e07e0d9b1af1c4fba44a97fdb7b99e93e1e20f684c9ea7995e366a8078a14c9a4cd62eddf17c4368e623de8e80"
                            },
                            {
                                "filesize": 3438673,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "5bdda313520a09ad0d3fc47b2c60d491aa4372a715f6dbe0a4dffd1f27af64d5c8f65b2c7518ff07725fc955568fba71f3640676c81d0077c069d9c5740d664f"
                            },
                            {
                                "filesize": 31358474,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "2638db736687056c762421d180e015a6fb4ae0a58726db3ec4e9a1faaaa531c94dedd7c7e69c3072a10e26481d6b1dbac1fcc07b6fc6d1103866f181ffabae66"
                            },
                            {
                                "filesize": 28902686,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "0ea4aac06dd1309bf1af458ce79dcc9f360214e5235a64cdfb10b64100676aa34f8dd286fdeab2d32c6001ca109398c562eaf10022679ccfdfe7e76ba07ed237"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "be": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53198563,
                                "from": "*",
                                "hashValue": "0f436f7b5682818dea33bcdcdca372e6a482c711cbf4a2a3441df11b5cdf1646b2e0531729011349d4811f720a31cb1aca249e67743b72babc52d04c01f6c0cf"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 31274979,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "bbd266d0e30ea49a978e0c249e5f510f814831a386f98d26f3ceba8f0aa6665d2e9b4cec3a39a60afcd06581507ae20fb04536d56741fa1f989b7113e5f6ce44"
                            },
                            {
                                "filesize": 28829892,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "602dc6eaa2f3d0f7605c2fdcd05da74e96670d9d4e7b82f8f224c32a2bc64062fcc34b13720b0ee089dfa4acebdb1fea15a20453fa9f050fbb386c0b7457faba"
                            },
                            {
                                "filesize": 22760566,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "6c55548652ffde376a7d16a1cf2310b4d0f648a022fa79f20067915c6f50972ab03146c037a6e37172023eb1bf266d2248de473b52379f31cb5fa7dac7ea6e6a"
                            },
                            {
                                "filesize": 3438614,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "ec155b09d5bf36d3d264f84092e81346510dc0f0f9018d710b944d278d122244de971c2c84428e096d797caa06e741f4e2a5a7e4b4747f4c7a8ed1d41bd761b4"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "bg": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53510348,
                                "from": "*",
                                "hashValue": "d9ccd33e52de24fb39762774c5c8795d6b7775a5e3d34a899be7cd2643c2b932489df89082639367af792d57828a2bdc92e9dde0dc605b341bcef8324ba18004"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 28997690,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "c7fd42b1012b00a26010ae5a47efd48f64246122161f0fc8960f22dbb5145d724dad7d6e2eb1635476ffc69561fe0b1fa05671ddffb6b2a834e62f38ef9b6afb"
                            },
                            {
                                "filesize": 3438701,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "e63eacb170fdf49c3e18927d3668b5124fc1a2d7c543e1e13ebd87613a89000557e3d5e7362ecc85a8f270cbeb5036c426ee4048343e7bbd1f939c81ab0a9c2a"
                            },
                            {
                                "filesize": 22842675,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "e2f5d634a1c576c6a8b2af4c5548b9a80f81df4002aca0caa0112d564a693fa49bd0de539ec36b0058bc52f85b5c0b5abcedce428e16f520e7def838e114cd40"
                            },
                            {
                                "filesize": 31404257,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "8902a96a1604c6530d15c3693dffcb4669bd557c6fd50a18ded2f96ad8635ae71978bb2612e21fab5977bb4b64d65e6ecc5e5f091e9c4a680d286dd27c307c3c"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "bn-BD": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53288709,
                                "from": "*",
                                "hashValue": "2b1c8eb7bb8fd7327e56f52a4bcb97f647e1e4e4ab837cdf62c448578783ff6c7e02368f94a12a828d8b3abf788f3557467ffabd7d41d28f35d01ce98792d1ab"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 31496904,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "936e5665b8668254850d04c5af659239b5991105a0dceb9fb9ab655dc8f6e90f77840850097f1cd349531586f249fed7be65513b78df165091732669ccdb96ce"
                            },
                            {
                                "filesize": 22772762,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "a527ec9aa8e78997212e3bf7b9fd55be601731e0ef0064c71c8d2a1835e4aab4132e722410c738b218d005640609987a79cef1954bde661acd8d42c251f55815"
                            },
                            {
                                "filesize": 3438371,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "a8731512dbec8a62ea8acd1f6d65f8fd72dc886bc8f78d8966eea3d28d126c3f3f4def9147740758e653bef6fd1772683cc4404cea31dedab78c622ef1cda1f2"
                            },
                            {
                                "filesize": 29078192,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "cb24fee7c665db4adff5ae00ff9fbe3d4e53d6505e73b262ae02f6cf7ffe661946e88bc6831472cb266727dd8002a717176f24dfb9bd64e1e5e29ef5db2d65fd"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "bn-IN": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53280314,
                                "from": "*",
                                "hashValue": "791270e694a98a85bb9682da546ea2e8e5e4af0ef36453dbe5bf8fe8abadc3832ec59dd3e90d86ccefc1a209dc4ea14b66fa9252fcb87a67ae17825aae23aae7"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 3438396,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "110c1db9f6e33fd9664c9de71ea81858c3417d12e9b9bcfaec5a775853e08dd66ec03f6de6a1ce34be68be775300b9b2b25a6b3feea1c10cb55eda142e080eb0"
                            },
                            {
                                "filesize": 22773860,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "6a9e864579b00d7ff7171a9470bbe054bb0e3199551d1964d2ffd144008b39b61f78fc863f6fd0aa3a4254ae609a151ca6d91ae86d5f684066a7bd213586347c"
                            },
                            {
                                "filesize": 31420903,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "c76283e5d6a60707c7c62a3669ae9b8084ea1bebd24c2f448403e847ded5cb680b7fc737e9308ed2a5ac41bf792d410d0d0a4f60ce5e3b274bb298113c34c78f"
                            },
                            {
                                "filesize": 29012352,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "ff8c69c2cee13bc8ac351898c5b2725e50b7b1a5bdc886be697793f3f25454f4fb36bda1f87759ae92426c65cf8039376b94ca278bc98c072c5b6db8cab9e330"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "br": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 54555087,
                                "from": "*",
                                "hashValue": "6577edf78348e10bee0d49989df5e47200a705779bdac77ce9f7148c9b445a531b4a97df2cf7e726b66aa687110065d314f898c6fc9a301f3f9002bed0136661"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 31287247,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "759a825cd96719b605d08b42b0080b69be8b86ace39471a3e797981400d62afebda0c1e6633255c3af835f31b128509c64fb638fe71767439388be20a07f9f69"
                            },
                            {
                                "filesize": 22758650,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "79a31b68be478dfb1ef7ff8ab04c5a7638d5aa131be75ac5411a234065a09c035ef64bc93dde429f3c639367aa71df8a0bbd33c8aa517cc887781964f42f7527"
                            },
                            {
                                "filesize": 28853605,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "a70309801e3118c3fc1d56c3ef339cbfa890ee7eac48a2c5c2ab0cc8dec2fa7bd3aefa8fca749d50955a391685533194b335dd03c753817fc98d6ca697434684"
                            },
                            {
                                "filesize": 3438408,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "faf200afb8bb671f72dc0a208afc7c4fef9796253460310e821018339cc18110fd4f3b122d29f1cf83bfdcb1c8ea1735234a5b91428d7897703127d8b9ca2cb5"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "bs": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53231839,
                                "from": "*",
                                "hashValue": "526d52f93a5d5bb9ce0c22ef8895e811fa3980bff807e098edbeda43757afdd7a06a206e0b530334bb7f447ae52d1ac289209bb06b2a7cadd147fac39e856bd8"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 28866258,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "5bee4b90d6827d5ee2079ff0c8f77b98545b22d5d9e4f5daf98dc7600a1594b882eabf23a58a2d14768b6583e021541899f1343738014e8715056f33e0202c93"
                            },
                            {
                                "filesize": 3438377,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "71de0a6f113fd69f0063ba94ab63fbe056436531947c87b8cf027ce7cc0346c4d76c45c42375404bf5826f61a6c08d41f47c8f8fbffb1cbb36d9394eeb08b358"
                            },
                            {
                                "filesize": 31460369,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "b0aac9b5f04e647502c091ede212d27d657b817a27a5c38ad9a1e338a8369bc313574f41c421af8f9fdb5ec8def383fe1ade7e13125ff1887453431f330e97c6"
                            },
                            {
                                "filesize": 22771886,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "a095b600a967181bf99307803242b4b00e84e75671621615c50d543284341e89ff322f2a34928e31c3c5b96402281b6cad34195f35e25f40610a3f8834e30af2"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "ca": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53614293,
                                "from": "*",
                                "hashValue": "49a760e7b45b81921cde27e46a5b132466a7995e5bc3e96ac810fc7ea263628735a17af3da0f496e9e0e496140971b895b524576cd6e56c2ee3cd0c998203d1e"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 28891023,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "f03954fa13394fae0d92c8736e458dbbcb338f7b36230397027c92459656bd7a206c1f73e5d92417a3c9d0c9c7965992c0371104b36906a408011e1519512154"
                            },
                            {
                                "filesize": 31327969,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "c7b8ef2f665c24b3d56a4f057da30e594d3eb944585c62c5a129d883a2db2b4c8537a08421d7afe7a05ab20074d83561253566b8cd7b490fc8cf42c0e28f3335"
                            },
                            {
                                "filesize": 3438415,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "aa725ca9b8d5cac1425af906420cd4f7a77184ef73503e3f161e3741bd1cb39a704d9b78cf8fb98e2d7a4064b21ed8e0d24080ff41e8752665d54d52a873a20d"
                            },
                            {
                                "filesize": 22797759,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "14de0c728ff2c2ed0a8371812dba32bd7a63d33fd48d19b38e5d1ed2ea51f2748693c6e0b842d108c546935158f182b07ab58b2dc0d2e37dd7b02541f21b4522"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "cs": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53198823,
                                "from": "*",
                                "hashValue": "e5db09233244ad93dd0a94f15382b2dcd7d0a684cc39be2c90fd576fea70e4c1e9d71be73a10c33bf05928100b8eaeb973bf4e7cd5aebee5102485c447313119"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 22780952,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "13c94c172cb2684eb2b9d59543883aea2d0da71b5563b27ed9e41c686ac1ce0681ba3308f156b8825d79206c111112880b8fed8014b27f14cf8c02272f96117e"
                            },
                            {
                                "filesize": 3438365,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "5f78b443afc77696c22d7bc44ba8a70819cbe2cefa662561a3b01d07dc884475e4e2c508c5d8748ecd2aa96b988af3e37daaf677e5e208740a9fd25a8b772594"
                            },
                            {
                                "filesize": 31330572,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "7e2a2c409b62503ffa49aa3a99bf2ccae9789d91ec35deb7c0cf4d44006ab722a8e3bee14541d11a0f5760ad050c41548deb1e8b39249f3ffd2388b16c79c55f"
                            },
                            {
                                "filesize": 28869629,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "e2cf4151becff739d75d28c743d52e1e8b08452ee786417529e300e13916740ca7816f49f11e193f5d6b38b15b039b242a4f3813caf7ffdfb4ff235791a8a640"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "cy": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53193875,
                                "from": "*",
                                "hashValue": "46a502c43454f037f44950984b42b180021713600e56511e06b0629dadb552c0dd651a24088cdd5cccdd76bf53c954ff828ac0bbba8e895f7b13ba04cdbd5d2a"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 22769265,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "7f5483e9cfae6e24864a327401d35cd2612e5a0d2fce5230b11ca2b58c068771d89fc9590625f7c5012fd8bfb9fd887835bcf88d4ee8a7240261fb86d27d9eac"
                            },
                            {
                                "filesize": 31293916,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "11c0e81a521ee38a95581cf856f84d3b07bbc27afad9597a89249875c1edb5a5946263c9e8142d72c4206637c1f7d618744d9399417c7288837261e782ebb4c7"
                            },
                            {
                                "filesize": 28849314,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "e1ac15583f6eb045f18eaf1b6b096ed0a1bcec50bb123974be052d51a4a8bccce60f029ff246c3e69df186b780a5ff9568dd28a4052a955e7d2137bdca4741e8"
                            },
                            {
                                "filesize": 3438350,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "2c4456bb84ecc822416d49344850695d4029bb16ed35c320e77594c6f0ce7ed2bf76d736bdce5c4eb06b286ceb130d4592f9c792ac06ba775b33280df10fcbc9"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "da": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53825067,
                                "from": "*",
                                "hashValue": "7567509e49c22b3344dd26e3818697ce944fef364e9aa77240108acabd457b768967db0dd8e42203f93c70589c9feda96330146fd5a536e60bccd375b4232ec2"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 3438368,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "6ff11a1cb82a19b423798d2999470b3cb4359fbdf13947170256e154584b05e0a4115731b0b628969093c0d679a17dc5a635661b5b853fcb38ba2b2861bbfc0f"
                            },
                            {
                                "filesize": 22759607,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "d11f274e1acbc3fb245cedbe509c0c0d4cb3117d90374c25dfa4c276a7a1d624a3fa74f7f3b9fd34bfcab876ddd7b0753778018f9f32cdc30356d9a38268d026"
                            },
                            {
                                "filesize": 28832528,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "3a812ecd9a19a5aabaf501388fee8ae75a8ff82a6c4c17c1dd64104ccfbbee300c36c1672023b62be78a145aae6f9d5ea5517632f22db4bc01d604bd4cecf7b3"
                            },
                            {
                                "filesize": 31288681,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "d5f793a2c70ec95547613f72a15a196bc6763c1293341801e1316453b88c75e14121b0f7e16522c1bdaf08b877bba26f625734f5c29b9ecaf92cf8ce105e1aca"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "de": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53203525,
                                "from": "*",
                                "hashValue": "536845a10304ec6aa44f147f08a7501299ef8137093724aed105a564e4236e148aef95c5c0a213cbeb913873d60fe1bf307f3eac7cb7d723946b7831407ca99c"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 28850184,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "bf0d71e58f0c04e6a0bda3c94db082a0b2913e8a7fffad651965f8e2fdf039ba494fdc1bdec82b428e973adbee6f77af49adaa7c2db86a070ffafb0f4066f8d4"
                            },
                            {
                                "filesize": 3438316,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "14cdb119576335d4b45031628ecc720d7a68d2b62da6083982f1394a2fc99c2a7e2170c6b2082456bd9088c44578acf12fb8ec441f0cfd845a90c906a47b54e6"
                            },
                            {
                                "filesize": 31292030,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "7c6ef10932c1d841243ee7a2456a33e9fa51a2ea459c7fa66568db09d2a904c284006f4f07f42486d6e694cde63876faf2b7b379a4da6192025b26abb53b653c"
                            },
                            {
                                "filesize": 22769531,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "bbfcf402d03146cc82ec07fd7fbcd198e13290bc97df06e91950709cbe2c6a8aec77a76d4c746ea6b7247d0394061137f1691955752a9bc2c6f7be2fca7718b6"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "dsb": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53219058,
                                "from": "*",
                                "hashValue": "859ac518cc59da7488518248d3acba990dee37ab0dd58425be0cd4ea3f2cfebada688eece27a2d51d73e2fce91c15b850d69274a3eaa59e8704ff844b0c2d96f"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 22775545,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "511189d561d32930629d6ad3f0ba0077b7130c51728df7a5f2834e245971a9b63e9ecdb10bb13278d28bd05d1c97ecc5cde450b1f69f66234cfa757a06a584af"
                            },
                            {
                                "filesize": 31299566,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "4f5fe3441880b083344dc4e55cc4ab3d95fabeb20b1c07ee13e8d40fa1dd02410045cf218adbe58a602ad0682654b7ab1b3b3b89785f38c69a00bf38d6784a79"
                            },
                            {
                                "filesize": 28856253,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "90a43cf6b12baf0b3e93106aa762e2f332fa554d0f10520df92acbdb365c6470e84dd947e72a7b7be1a6ca20be7dbc5f4135bcd70f94c04121adf21dbc4a1ec7"
                            },
                            {
                                "filesize": 3438426,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "6473df7f300736f6dbfb4d0ffdc7a30194caee6549de987a4f79d42a89ce8b8503356913b31f52184e07b2450685439481402acdd38f1c70e97afab2571c10ca"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "el": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53246755,
                                "from": "*",
                                "hashValue": "c94ff923ed14c10e7ae8f0092a41abb3883fb739ffe68d597f2e51b8c13d1bb32ef1885b443c1707002c459b6edadaecd81839d81379a75832fb96a5a8ff6b5c"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 28843344,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "b80ada210313f9de273cd4c74e78fdee47912e1095b76d8a69128eb190ca2d1181aa6c50986c26f9cdf5dde1ea44e1c5d0cd4e982fd5b088bfdce2c3a0466a83"
                            },
                            {
                                "filesize": 3438459,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "b02a7812c4f0de775e9c17eec6781a1142efae8d9695f92a63e021e3dea85645023373b6cf5ddc3ca49e090e54a00b8821dd3cdaf23e16923f76273bd71f9988"
                            },
                            {
                                "filesize": 31298558,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "a47089b960b34ad8d2fe0a009f53d633d83411980ddd38e5fde73c5c97f97d886ffeb88b67b798e4e3b4cb125a365e9c9cfdb57c85359051c2c738ee5fdc525d"
                            },
                            {
                                "filesize": 22767187,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "b4e1bff9863ff25ef056929a6143acd0afd409da9d612773256dd13ce1a729b8d6e343363de00d52b00f4d719b34415e7d8807b825b7a494b68205e01c2e5033"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "en-GB": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53181386,
                                "from": "*",
                                "hashValue": "3cd5f75d53e61432442af4a56342b1d1f50df7ba80529c25e3a4fc42319e8c8132892d585297202fcd60697f671fc37c16f2fbc6b951a684f5a2a9f07df3d395"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 3438557,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "8113b54075318096ad3012d0ec190a9c6b33babc8499fc7cfd82bf82b334e366b4089e994b9d04010f9b6b31250a909095a4789857f3022ab5eb290936ea49fc"
                            },
                            {
                                "filesize": 28859820,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "4ebb69fc08790fc9bcbdba78fadc7ab1a5a877a90c3d77e88a1af342fbfdee7644974253d2caea12b34603d84ea99a0d1b49209659c5f7dccd4f7e0d1ad4c357"
                            },
                            {
                                "filesize": 31269420,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "f01d4c699ab06a0930aca3b8c3e3a7716cac71a14c8190af5ee123dba8e14a1a5d5e4c691c4636388b258403de1803cb10e28b3ea36349ae8e3096ac9f390faa"
                            },
                            {
                                "filesize": 22751503,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "c1837710d10c0e6d41d91ff51462b136f6d1f1b3ef1ac3cab0609298caf21719f81ed7555ffacc2569fc866f6226d2adf811d88300babb8d9329ea32d5422267"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "en-US": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": "53458173",
                                "from": "*",
                                "hashValue": "619f9765b667230838bbf8623d1d393ee3e67c7fe577581b21f1c1062f1d9f0b0950b39d5d764ab163c0ad80ef905c9c52aa4b796fdc7340955020c2be832837"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": "3438460",
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "ca24b67ca1802ca9025dbfae84c8a5ceded7e2c8668d84cf650c82a05958cc0719f42bd27516d0e4ba0bf7dcb2e4107b0216f73b9f7ecd9bd87a4c36efde6536"
                            },
                            {
                                "filesize": "28862041",
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "011e045465a3df7a6db522511bca661ff4ec4a6754319a75ec3bd16cb0fa13f7989d9a617ec8c4943ccccd472dc1957ceee9d6658f56ac48f7ed9f6fcc1683e8"
                            },
                            {
                                "filesize": "22781177",
                                "from": "Firefox-42.0-build2",
                                "hashValue": "41a79a5b948c0e00eb49ef112a87829782955eea1afcbcd8d6ef8858ac7b5a6b284faff424c34c7113c59d1a5cfdcb0c6419c0fe15636306a1437d9f7bc46106"
                            },
                            {
                                "filesize": "31304649",
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "9dd7585191db287a5334a80542da742b79ffe44bd90489aeadb18d7e59fac46be4ad72adf4f565c42d1eb94ebfdc1509b97435c2c346d70cf4cb20d8b8043acd"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "en-ZA": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53186776,
                                "from": "*",
                                "hashValue": "7eb158792644068eb64be3f85ca3fd8bab0bdb34ec5c555e11b5ba236f4b0dbaf687b88fe815b105983132dcadb9678c9f8e3685c906cd68b362977e34a32c54"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 28835966,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "567f48dbee80cfe1f63ed112bf50ac611433509b5011577823be90a47007a603c902fcbb282172c03f096e612a819d3f22d2662d195193d328e4583457b351ab"
                            },
                            {
                                "filesize": 31268152,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "7e014b3eed72ac3ffc55b5e0615ef125025670745ce8eab3637a9f0af4892157f79cc4021fe8b505b83328aaf185931471ab0da4328b6213e99c2403f5582608"
                            },
                            {
                                "filesize": 3438548,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "91804d4225e0b6a0996fef9be6d1b5dc65be0dda7e71e8b0e439bb7e760eee9fc913dea0a9911ee7bb426708b92e21bbd72de3f08dac7d8c474251a596a54551"
                            },
                            {
                                "filesize": 22760327,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "9299bf7c4c4877d063e61a1a83fdabe3e05087c7a045b3f9853c637f30af00f43cf932f7ad46c8634aec2ef367a99523082677ba939859d36506739561ea379b"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "eo": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53231132,
                                "from": "*",
                                "hashValue": "097eaea91b9ba995acba6c780d8e7b7d827f6ff09bfa90dce2ba831bdc99ff26db66ca3e065be9bfe7d5cffcd8d2cd0da1f8f55cb7a886d5fe3bd394be19726b"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 22776869,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "418b9f4bc9b2fc80b7564f5b1404fa6740d39a4fe51412a3028838e62dddb57812729c8b345813337f16392488e6594648e809443bee701c07a9321b06f9e075"
                            },
                            {
                                "filesize": 28859490,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "d35505c6dc7c5cf997b1ca24632dc4893257d76c223d7d093a29c412cf43ace476d230a9ff3feb6b8c512a3e277c42cf9e188acffa359ae3b5765a83df38cdbc"
                            },
                            {
                                "filesize": 31309859,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "c8672104183704152a9115e84b1b08a32b77f4f4b26ad561782350faca11ee7b57ef1b36361d46ce7a43fb75f7149644c654d2cdbd8ab76a7791a61352564a05"
                            },
                            {
                                "filesize": 3438552,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "b673986dea9dd6e89b3da2c4da1669ff056abdc63617585ce61e1a1924d12ca6617a74a64c3740f549563da5a2ea897624ff3b1174e2434dc55af9486dbe99ed"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "es-AR": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53196126,
                                "from": "*",
                                "hashValue": "ec0e452c28decf85ca8abb0c8b21fca84cabed6c4f3f41391e23d4945d04df5a860eb00337e1ea83bb371c39d7edfe785776f920bd91d304615ef791a0c4c48a"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 3438529,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "157ebc1b9e55e91e17d469ad536b22bb7621d2ec2ecc27856ae8718800e9a96dc6b8b8095350a117d365054bcc314bb36e1fbcb738b686075bdfea924dd7dc52"
                            },
                            {
                                "filesize": 22766413,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "2d33a2b1a84584aa44b52bc11cb4514e20e5e58b17ad29b3f3bd60051bd331e813fbf89f118bc17360c6cfb3c838c9fc7a83ce87ae419f101ada7799bf4eec34"
                            },
                            {
                                "filesize": 28849324,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "f41ec132bf78c747627a5a479295ca4aee8a4682ca1a5f76e667130207594b653e81466b2aa2d4bba9cbed70cc6ccd5f4be7e80880d8d67cf489e3fa67504a2e"
                            },
                            {
                                "filesize": 31288972,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "ca65324836172867a81cb5e9d3a8cf52aa94932a8fbc86883a8ea33dc820d7df2c2ac5e7578205612fd018285e2a9001d39141465d177282075e9c88fd06fa45"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "es-CL": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53117945,
                                "from": "*",
                                "hashValue": "ffa3e0f9706b90d2dff58826fef7591438fe07bfde6c34c6581973e510fad7343c121afaaa8446f84bfa16a81efbab5da6c7b11e0e02af4973f270eedb1f7cda"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 22736029,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "3fa009ae3d1c519d2966f758de86700fba8835c230d10a460a6c1d524d507909939bb0a6f7aab0a4c0ba3e5e07720ec35bbef5194b8fcd5291caadcb448a1f86"
                            },
                            {
                                "filesize": 31245324,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "6df1b523a57f246578c3ed68f4d083cb49605c831389cddcd607f7e3dc2ebab3055da17968a917c16136dd22efee656a96e8f5896196859ef4a3b435c77ea584"
                            },
                            {
                                "filesize": 28816135,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "f0711e3b2bb235600c1efc2ed0f8199d6454ae762b0ed903d1c27499e66a4fabc221f978680e1323fe00481c6cda5306a367652fcabcd5e5369d8e08f3f80421"
                            },
                            {
                                "filesize": 3438540,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "7e32639b1fa32621ec2262237dc4abdc51100579219166ca9d9467fb77d94b082694ef0ac64d8e5003e81f4d506c6ffb863663d5398ce1b2bfa670b512673942"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "es-ES": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53102813,
                                "from": "*",
                                "hashValue": "2d47a7468e5572da51ee7abb18ad3268e4dfd7ce2c566c7ec7f661604fe22a73dd8532fb125051890d75eb1583e28ca5c02ea23c2832dd9c31903cfe92d37e16"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 22726586,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "61542df90bc999300a4a70def6a054a2a5b7d9b24a2ad10e6c6142dfb08cc2c3f47669e9c1b456a90e1c3e6ccb12123e6952f36f9cf0f73ce85edbded9254178"
                            },
                            {
                                "filesize": 31232311,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "9c3ad90f1e64c7702df8dd274cd58d666b583ba3d83541791fcbbb0c4adc4cde1251cc7f7fcfa36102768f84c37f9877e98d3ce8a38903d8b55bf3bd7c21eabf"
                            },
                            {
                                "filesize": 3438552,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "af3212ea3fa9617912521cb401fe266a65c61ade380aa4bcd19f9a69af5c794f7ef90f94386b540378005cee84ec26c8b18fb7eeaa7569fad118215755fd01f6"
                            },
                            {
                                "filesize": 28805281,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "a2d11d49712f6ee137aefc4017e2e7807e5c61d2612aa50dd89ea5e39a893124fff1b6317404cb1188caa0b79dfefc9efeefcc2b99ee59d82b90a5bc5b5d2b36"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "es-MX": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53200993,
                                "from": "*",
                                "hashValue": "1cf327f7302f87d63ebd7a58005fce46239a71604ff580fba7a214037632044ac34f29c10e330722888e7d4e53b3a2718ed79c7705dbf3b11e28ba20bf279fae"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 31337503,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "09c40d8c9f9ab70c5a4a3432e6372a5b3a1bd80ab32fca8f0151d1bc81db355a58b86ce0a2e41cc8110a16343941136454cb8167b2cc8eedf1bc2dadf2cee3db"
                            },
                            {
                                "filesize": 28853103,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "75040ea5e2b3c59fff0caede457ed5e039624c31c6087d82540997d097e1b5fa67ed3313ecfdd2c7cbd89d55147c35727673bff4abb4d7471711725d9a480217"
                            },
                            {
                                "filesize": 3438566,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "4672905270b5aa05d2e695c583e5eea25fad0c9fe999541fc77bc134188de13de703f39c569a82d56d13840cee65c9d0ae19c7dcd7300ce680f6a80c3dbee370"
                            },
                            {
                                "filesize": 22772293,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "34cd5d28faa55d9fd7c8953b53558b74a25aea36e793f7aafa0f6dd24a0fbd4e9521381c1578760f4a40133250b582bfbcfd563bc45b77ec59867dab06993aa5"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "et": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 54028239,
                                "from": "*",
                                "hashValue": "ae5d5ede7faa5991cab29186901bf3d30096d8ab690c05772281a6b7b8ecd3e06d78875a52c4a5b6451655ec2eb9ebcbf001d17733372dccc8eceb546c36b478"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 31281022,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "a9673f7dedb7def3ee273d6b3b8608349c3c5f1bcbd2fddbcaa55bfe18abc5509ca40c2ef8c51d2fe0c58c8f7585130776e353f7a643220305d6c54121c51d7f"
                            },
                            {
                                "filesize": 28839429,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "e01227e621527ee5661d4f763c722ac386895894fe72abbb8103efe54998ef3d809a01560564fce4b44002ae9cc5c1eb6d3f34d1e20ecc8d4daef395b5d922a2"
                            },
                            {
                                "filesize": 22763434,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "a801ec78894e60790121e7eb51c484e0450133d44b3e9666906a2eef6d45c22c9b1c9b99c1250bbf12449545e8027e38d94d100c213d1818ec4ec8fdf2ce0e8d"
                            },
                            {
                                "filesize": 3438458,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "99659af4af70c29c3160f58246160919de7b9a44d291a36f0518d21473ddd7629de293f7d58b61429fd3a3421c2b8a361cf1fd83eacc6ea893a7b9a8736f51fe"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "eu": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53213866,
                                "from": "*",
                                "hashValue": "c14d9ac77baef757e9353ea7e32893cacb47c7828667dbff74f8af83a2c799c476d7c445f4ed7b06c7c5325da8457e4b6f876ee80e33e1781daba3f9e4fd3030"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 22771796,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "bcf1b65479c36b9342dbd93bd954822cf88bba13d5a6158aaeb66093f4dc51e6bfe3b4693c977a7c9c84197c9739c95eb49a6d440060ca633f86e894beb90355"
                            },
                            {
                                "filesize": 3438616,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "539af8453fbc1d61e7e319f4fe3490e4f4b6d3f890da8a8a9bf3bd6b097ffc820d65b54af77f081ccec9c538069cd01c24e2e95686b2c2a01ea2507dc048b0f3"
                            },
                            {
                                "filesize": 28874401,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "445d959b1d4b863de1c116410e121aa63c45b3e878421948ac70f0cf0d3ca2fd8e2ee4a04ab1d3a83154966619cc239af1906d564e4f82bd205841ac07804de0"
                            },
                            {
                                "filesize": 31326432,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "593b54a2a5b43bd8a034b0e5fbedf088ab3e485589957ab73c9c0fea894d014e1de41304923958a53c1876b8717f996789ec1c172de8b480f9337dafbb82310d"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "fa": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53269260,
                                "from": "*",
                                "hashValue": "5150d8b871f97778635464cb329673fea0da4c9a3f808f391cac9acc180cc5a948e6a584c29c620bc05a8355be56c8e96fd9ca61a3b585e4601ecd81c36328fc"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 29007516,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "f968b2b893b57722ef3a12b3bee8c9f680acf91849b1d3d1b0e00c47ee9cee1bb13e66ac65c6856c89cf684f8d3a12b9b2be65ca685c2f476d5dbe9c5a5bd157"
                            },
                            {
                                "filesize": 3438585,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "fbe54b94fc3d473c17a9c3f70210767f202bc0e28c53c04dac7b8204fb2ac4b4c10f99596e029b64fbca9237971ec4be0980b48fb4d36a06d89930a2ce79d7f4"
                            },
                            {
                                "filesize": 31424478,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "5abc9fb24a3dc50fa21629203cf0634479d2f2d816a0d4b35289a16a1448b68be54f93ade35c18e28ca835876b12a0cb626aaeb046530ab2ff0422ae452fed61"
                            },
                            {
                                "filesize": 22872210,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "ed614681da3067674d860e01a058e0ca2ce4e16f66febc48744f58ecf63bc43314be7a5637d3f3d96b477a9c05c87b075c855022c805cc7df0cad99d6bd08fb5"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "ff": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53201757,
                                "from": "*",
                                "hashValue": "09f2487a0b74612b57fb997485c061c346fbccef1630b24a303c68850c5a776f41d6bb7ddbbdb88c1045227bae263387b09369a61a0b846e7b677d2d369def9e"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 22756003,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "ff7ceaa65b73098b0246993b84f8daccc1bda2a549f99b961d7e49ff2d7f4c8160eec4eee9d9a60155d0347b7704c57512e0f41a69caf6c7ec20b270b0367411"
                            },
                            {
                                "filesize": 31273952,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "5c816c17a36f9a9c915c7c9fc6f1ffd54bcb557af57ef69baf73f7cbffd977a601aa5240c118f0d055e151547c2be0105afb99a71d690fa756a9648d5ba0b805"
                            },
                            {
                                "filesize": 28833658,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "a07d2962134dbe335dfc7984ab3dd3760e39329099af52cea55ad34b0de558075966c8ada8ad9604daf02a02818a5d9faf9c62f0bfc5dbab8860d3a16b142a7c"
                            },
                            {
                                "filesize": 3438546,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "b06a9621201e353b29b5b10a5da2c2161597000deeb152eebe6a1b5cff70b1c8d489dd692af00989221608133a165d76b7e61322c1db2f8a77b62bb841a0636e"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "fi": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53191674,
                                "from": "*",
                                "hashValue": "d246737b20902f2427404994b647d8b7fdd99d273c66db856e490264beef2bf039773a3ad10b31b590344a2e3567e2973f671cdf299cddb238884077073d0b49"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 31275856,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "396922927387e789f6fdd8a98e192a3771254fc3e02bdcbcd5e6fff2f57ed2211ffdf2f5cba62b8b1e72d56a47e7f08c6cfbdbea25b276476e3948370b0522bf"
                            },
                            {
                                "filesize": 3438585,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "7c36304ad21ca1b54a67689b49d836a89e9a738f5ae32d2496883a6650ab33f25c1e444759977b1f03c23da5c4ff8d0437aad2b3c30819259778b2e0be23ce35"
                            },
                            {
                                "filesize": 28839348,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "6218fd568072f4953c5bc751413c6b19aa7dcac37f9f31cd0ea71a1bf99f3295c51d300ec35a09d128f829914fed5d1eb3fc8032ee96589e132420f530232b00"
                            },
                            {
                                "filesize": 22763352,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "f8c03f78ef104ae869958c4096d9c1cf2aa807c8f61f0bdc25760f70dbc60d8a8d13385901f5e8de2a9a76df537133237a7f4a3bcb8c4cd74c1fcc8d6ab96e39"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "fr": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53573742,
                                "from": "*",
                                "hashValue": "12828f17a2cc940aeab8228f82a65087719ddb4d987b703c313272e77b0a2e74837526df8de87ca8ea6283812ce40a2270af741cfe37ead24ad1ed045ba6a267"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 22797478,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "d3c817588776f7ebfcf5ebde833561d6dd15b79733610a166c02b49ed479628cf80f1ef619c5d5d2f43a3eec5864849b3127c1c14c9e04d5e2e687f00893611b"
                            },
                            {
                                "filesize": 3438556,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "4770f43b50ea3a7af6f9f9e002f813ba498267a13337d944c8ca04020543da21e5c1810c1467f949c92862c1e64cdd1d12fb6e425d03a8b4262ee36e4bb010b1"
                            },
                            {
                                "filesize": 28874420,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "13d999de6edaaa7fe424a0f70c452c934ed3287b362c49657581177649627e28251249564ea7c26a56562ab86c32f65976350c0fdb362446ed717dac8cedb12d"
                            },
                            {
                                "filesize": 31316053,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "df788a347dcac7d75b016903f54c2d9c8fc97861eb007a0f055854603c9216a6267ac3692a3edc052942c4ef3213a7c3fd27f9be237d44dbb4f2b056be8ce66d"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "fy-NL": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53201027,
                                "from": "*",
                                "hashValue": "082d5eb9e7acb59f045798e56f4590d0289e7748d838d1b81e8d300919c3f90c6667dd59223a605c6c9007cb157ccad90d7fe96efc0d02a9e6de7d776fea6896"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 22780997,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "7cbaa7efdd453700816f3f9c998d87acf4f34ba06a272032823807f141fd6689f7e23624121dd6dfae76376c6633d2819ce0c14d3522758dfa72f8722b9ccd41"
                            },
                            {
                                "filesize": 31295878,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "d127e7c19de206464da772e5903d440710823478f31867bc90abed7846610546d3cd760287597026c4dce9a19f2b9b6cc3c15323b2cf7c27f967935612274e1e"
                            },
                            {
                                "filesize": 28851430,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "68ae806a9ce89eb1179f8f180fcc35480c51145bb88d51ace5092abb0b283fed078675c98815db7c72f9e97f472858af5fac39261e73851f356042b248c02648"
                            },
                            {
                                "filesize": 3438495,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "10fc762be97e5e21baa63a21c6cfce4070f6e0aa98c150dbd358cb5e7288451bf582e999fe89be4fe0d02aa29b807bb09feb3aa5a4e1d607d1465c3660e103ed"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "ga-IE": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53214577,
                                "from": "*",
                                "hashValue": "e9eb9d6af7d1c3891807076efcc945ffc2d57544f1449de42fde1fe9996b0049e839967c6d0d1ac0b29e221e26e75845acc762b0a0d960d69287c97c390b6cc1"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 31302209,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "15214354d5e256a9fbe11df4dcd361fc9925022c8a00aa5d985075a151375d41e3c91d10ce10da7e9f32405b7184fb71adf50932c0355232a6aac7505be3f82f"
                            },
                            {
                                "filesize": 3438535,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "336ca46797a9616989444bb5980fffb52ef6f3cdb78ae1ef041ba717bc0ff14e7a457d91a82635c0365a3e8e62c6ea4f0aa2dbbc359d0ff6c28cc65986d186c5"
                            },
                            {
                                "filesize": 28864905,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "c59664b255bf695934d367dd651bf4a6b72ab501a1d5989d6673ba204e4b8f044c623424fd47a59365a352e39dd2a0c47b46c57ec95f3a3a200b3096d83f4e2f"
                            },
                            {
                                "filesize": 22781953,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "71e5fb04dfe32c9194e994f5bae81902f8b77db8daebb2887b10ca4a6bc6e301960aaab4dc894a334ae5824fc811710ffda6dfb93676d555d0dcb7679fae48a0"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "gd": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53202657,
                                "from": "*",
                                "hashValue": "502b4925d0c17debf8446b170593e9669ad878feca6ee33ba7c9abd2528797203087c2b5ce6d718546c9fc2f75f258db575402dab7b29f460537e0d37eb342fd"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 31289967,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "899cad411ef1a83109149911789039e69bab436dde6f2c65ae1eecadf356b4163440846e56e0dcd485ef1e4357d019df7cba360a045dfb7f0b4d30aa63a335d9"
                            },
                            {
                                "filesize": 22772835,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "ffe2a57d2785fb60d5516bfade9036c86cbeb7bbf5abac4c4084281b12c2882b11556c9fa9d9d32504a6c63a01af0b0fcb6143ba80915663509a12b8667328fc"
                            },
                            {
                                "filesize": 28856255,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "99c420025b4c47409473b7c99a4f3bc40ced92ab94beeaff0927cf729d1cfd4c947676cc0005c4b1922e010de63bf1b56725800258ae2bc56e1239aab0e7b4db"
                            },
                            {
                                "filesize": 3438579,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "c0b1676125a1e9dc73f923bb659d683a212880e9e76e232328d819375f4744cc8cc0fc1c118896ed667e4bb3f9d11b969b3b9c90137d3a7495668de18d7d9632"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "gl": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53191492,
                                "from": "*",
                                "hashValue": "40dded65f7e7f95e4479502b990a6cb0ee691fcfaff4825424864ae64360dfc8e6bd775c7b8dbf1cfe83f21df2c8f9e4471041b914c60d90fd5b3ff7de89b044"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 28957015,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "fe9baedb6e61a2ca37cc052f057e01fbbceef15b182214c3cc180bdd784df64b0e484682d477d3ea0ffbf734daf01edb9832ea22ef92752840c9c9adc1fba5e6"
                            },
                            {
                                "filesize": 3438435,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "480f13780a86274347b8e665f1167c22d108fab936583a7368d51aa73af47a2dca6c1067649da021a8775a783542c03e16b3f23d4801b4b9d19be7657a717778"
                            },
                            {
                                "filesize": 31366171,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "65b509027247b63e05a38d4dcbf7c62b7ba1b6691cb5be29471e14b7eabbcb874c44a45dad6f411af8efdf24ca716469525731736bb8ebca885c84e99a5b3ecf"
                            },
                            {
                                "filesize": 22771291,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "e1ade199d3f9b6ee0f917a9bc8b57de89af0cc5a6ea8e6c830e11f3676e322cf803b810983f94589c1935f2c8cee2ab88ef73c200639a443f98f5068488ccc78"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "gu-IN": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53231618,
                                "from": "*",
                                "hashValue": "e76125ed6416a0e4bdb40fdedb25999a4f24fe5079d0791f7834560470f2bf3eb524e4d5500abe484a347c1fcbddb63831c5edaaff85d3ea5caf4d2cc381cc98"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 28828491,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "457909a4da3c966400ab93f393550f59a8652f47ecbfd59da3c33ff3418c7d9f11997a9c68039534888852357fcad631c5f7218c8dac5d6c54bf635b3f3b4231"
                            },
                            {
                                "filesize": 3438437,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "d41b29bc3ead91366b43e5116dccbb95c2853d3d355bacc0b33d68d4d8cfc94c0e5431d053fe73cc62448e723b18e816a359ccf94b03655cd3b1bfa732c2b786"
                            },
                            {
                                "filesize": 31267311,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "f41a5073dead872067ff061b4e2fa71fe4f7efe8d3ee0ec5e85cef72d3f3a772b82ceff958d8dde4e74a639b32b3964e2d3110d44d8c949afb66a17cad0b9a21"
                            },
                            {
                                "filesize": 22762994,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "ecd921607c1cd365fc7e3e79d2b50a3647fd81e6e860ec41a051aac5fb40631c6c71d223eadbc9cc81706faa442cf1146c3f4dbb9d088824c943fddaa31dd751"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "he": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53221576,
                                "from": "*",
                                "hashValue": "18c80d2c1954e427ca5b991a6d3b2f1e50e19629bb23259238272f9e3acd43eded07cf3d3fd9ffa1e43da62f4016696a907b1c20add29ecda063a676c90f99fb"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 3438387,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "c1a0ece992c55608b138e5eb60c2c42025c865938c2752c68b30b1038c78ce20b0d9a7b33b826dd1ae6df4c2491fa7388ad4cc74d878f09b32e7727bf8cc1a63"
                            },
                            {
                                "filesize": 22772375,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "fe91acee417f8f89729e86e0e6338f50697587973f5d1d6f665e13c961ea54542f888c4ec7413c0899dd450897b61a34e1064969ee53642d3a84733e503b9450"
                            },
                            {
                                "filesize": 29007386,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "83f3a515fe46eefe606f640968a2165e1eda5f06ab97cd35c927643ffa9480b5ff4544f5884f760e1e37f6a67736ad4610139ccaa28b8cc85ede5ebea6097528"
                            },
                            {
                                "filesize": 31426693,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "b6f8aed8d872e543ca57217eafa84025e95b3ee9fd755c271e2e7a1b1f969fe5287a058ad93e3c7dc25b36ec1b83def24ba2d5a22af98a5e1d978d6d1a08ea0c"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "hi-IN": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53255815,
                                "from": "*",
                                "hashValue": "e6bc5d3d031bd8b7183cad577053cedfe8627577c5c666c1187865de5e23bbf77c19669148e17abfb3902527a11a9fc609c94955c9c61bb6fbd0a70beca6604a"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 3438387,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "b872383edb5a91620ce9495bba160e8bafe1e0e5f43d2417b6211cf261f9dca1688dc5609e97029ace942b2676065f248769c2e08cd137816b5370bfc5aea53c"
                            },
                            {
                                "filesize": 22764764,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "d0ad205646b97f5de6f0c90d1079ad8f4707e653e563d20e87e818f3e2078a3be2fe77dce5aff88fa41009b4bbe10a3cec6c9d45287bf05790f25d999b6b7cb5"
                            },
                            {
                                "filesize": 31292103,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "ee6c666391c9160963f39067bdce346058b3bbde2d33a3864fc91969fa3f52df871a99dbe06570ab275abaf9386eac279b7014bbb12dbf6188387ddade275567"
                            },
                            {
                                "filesize": 28830036,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "c5eef5b41b284d015088fe9dac394161cd77718de1f4ab31e9db9cfb0cfaacf4bcda5dfcc6127375cc2045a9ecab667b2390ad66d0c0383d736a2effaaeff4a2"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "hr": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53225941,
                                "from": "*",
                                "hashValue": "5c939052272389b707144fa709973cc7255628bbe71857838e602a7972c84838651a8e6f45e9db1f9022c47454090cb90b991cf096258f533679dd11f09e5272"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 28853633,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "a58646c102029fa8ca27cefd10fcd47744061b3e0a37fb70aae0bbedc49d4803293032b166398ae575af0ffb8777c1c35bcaea42f0bf1f8809d0a9369adb0282"
                            },
                            {
                                "filesize": 22771253,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "42ee59587ac81b3166feff01197bf89338f6ad68b674dbfad94a52fb642cdf4787da9c4618b85d63a04706515decc51838972c299bc21dad0a5a4f136dc3ebf3"
                            },
                            {
                                "filesize": 31329411,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "997c352c32e6f5bce75fa8a4ab6be876222e15f96e24d95244e7c370451ff074ad27a2e715492ea923b3236eb6e6651d9f71642bf24649620f4a9ea93ed0ea65"
                            },
                            {
                                "filesize": 3438380,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "f0eb7cd8074fdfe3d5bab9b85fd39de8079d18fe579cdbe3e7d8d1e47a988743c1204a304ce573d57212fabca61d043369a1858fd2723786cc21a4016c7d7d85"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "hsb": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53217726,
                                "from": "*",
                                "hashValue": "94224ab26cae2c7d6a06fe270ec32c6563ad2f22504cc01527e05c23f6a405b28a69777e3fb593d19fcbb14b7f328781508f8fe53fa32cf679121d63401ffd0c"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 3438359,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "dbf9b419bdd3e73cc772b12e540720d9c35d7908c80e5475bedaeafcacec2b9e8da9bfa0b338e94b0ed0cc99ebf615175fccc2b07b7687e755a41f5473a26569"
                            },
                            {
                                "filesize": 22774871,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "8decbf1aa8c646dccce80c6fdb8760a3965086dfa89f3e9f9d56d014045786c2e715c634e963068800d34bd48c1f9a5ccdd83615aa96b5978bf537d999084d3b"
                            },
                            {
                                "filesize": 28876090,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "54d5b96e1863e8d3a945d07a54122ca8ab4dce26a35b98f04ee1b340caea09a3b138d7e91a3f07b8c37acee0269a6c685170e9960b331acd2d8e7ee1abf9b743"
                            },
                            {
                                "filesize": 31317152,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "49ba89165b01c9118b9568ce62d264ab8322bf0fbd610cb785127b6ae8e76470288844a91eddfb3f6fa248118fcc7d3195e87f39b26e1adcd2d0f5ab4b6aeb56"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "hu": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53827748,
                                "from": "*",
                                "hashValue": "041794a5c43ed9fd8e31eaa470be4ec2694aafac514e894b41138006928e1d6f359da374bc636c3e39cff45266f20f8308122688efefe398dc3e216bd9a0e78f"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 28846565,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "98c6e724817c943d419e653687a7d6b056511a191e883dc2690810e42064462bf5100831a3f0a975fd03452afb3f9ec23118df274157443dc805da1e822f344f"
                            },
                            {
                                "filesize": 31295746,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "1ff2dddb0ce0441853b61d070cb23a6bdf08201797b4c56f27298e425afe554a51b927f55394baf6619a71f24687b390bb2392f934c82d78e821f7ae658f2c0c"
                            },
                            {
                                "filesize": 3438356,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "530ac004b4e6ec40e859cc219bb08944fccd6d4e85703933ed3178960935f5de04ffb0aae69b70df7843fd4c763566ede7380205f9d5362229af2da086b63332"
                            },
                            {
                                "filesize": 22769189,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "e26832df3e48c06ae828db3236f63bd0f8bf0c765a5d0f6d6a850ec66e8b5c1bd7cebd5e451f4f4f93207066760872c6c405f28435a46cd5f2f94baafed5c28b"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "hy-AM": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53284935,
                                "from": "*",
                                "hashValue": "3da3ceb0f42431999dfd62f0a36eb66e8f508bc2aa82c79459eef6c94284f5b9d3247b7c4ab855a922158a8891ffb73f821236d341af4a6e9a7d8142b767081b"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 28943852,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "00d84054e5ddca7dca8658f24e54e8b14babfe6f378b264b02cf149dfef73d34b8c65ea0e5dab2771755fbd1c46a193db8580d8b744033743631e9f3d1675404"
                            },
                            {
                                "filesize": 3438360,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "dbbb0c806a1c0613c7648195987ac6ed25ccd5996ae64bf27137ee0ccc5bb0618d26f5f33dc8f4d37458cd2a7fdbd2e700107bfa814cf04ef2bf1d07d7a47ca8"
                            },
                            {
                                "filesize": 22754337,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "ba7e23ee45bdd6731f28b4027a75168219d4c56501828c83bfd5e3c8c2fd5e994a451dbf6b56121a2761db983f053b71f0077c8325cdc86e9e10c0404270e800"
                            },
                            {
                                "filesize": 31387372,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "7f8ffdcc35fc8d7250cd1b1c6b9979c47b457ea137b10483910b198123e627c0b56ffce6f79922937f114d1a64dd2e872a9f8d747f91d759b2706aea68b50c9f"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "id": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53273113,
                                "from": "*",
                                "hashValue": "ea0e44a6dac8723eca9c927bc26ba4a197f90cd58f60b10e9ce2684337463e7532195827fb9ddd4a8099bce7abf9fe73195b2d5b63ded46c6442a1e5934ae7a9"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 22754234,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "f1d4c9add986fcd11e347450e3900b096e05af7f5b6f7078eae47815622ba7c5c464f7f59da4ad227ca7310bdbd5a9498ee8e0e68c35379969e486e398c95b51"
                            },
                            {
                                "filesize": 31299161,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "98361c261a6ed7d0692c329905d5b6a3db1b1c1e3cba38bebd9eb54c26b866035cb0a811c2d9cfa2bd2e16bbafadc34b6bb82358bf63fbed9d873e512fd910d5"
                            },
                            {
                                "filesize": 3438345,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "bef8ffdfacaa9f287761ce2bcb06e4b6361744eecaf88c7f57a683ba8eadd4de49c891f59ebb1342b3d4bad8a2db772c99511cc5177a789f422b5d1d7d572151"
                            },
                            {
                                "filesize": 28852697,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "f54601dfe3a6de65e46e6198d2b0326bdbf2d38dea86174a7b798615b5a2697edc776828e72ce672836420ef3b525d213fdb9197f25a10a923631d7e9e68e1c5"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "is": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53233956,
                                "from": "*",
                                "hashValue": "d795c698a23bbfe9994710e3d8f1bbfb0daf5c7ec7eb44de5b025ccfd15118d25bc06aaaa983393d8bf80d99a08d3da573782c6f483e85170c33df6e0f4d5d1f"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 22766250,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "0212d291d69b5e0d80693012b371856f2d55876d51dc515cfe18c355fa65c7467a55a90315fbb3ded6894f99726174b002aac5949ffa239a7bb897afc153a72a"
                            },
                            {
                                "filesize": 3438436,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "2680017e77713abc3de6d5e3d274b5c3ca2df117009001dd4e79db2d19bb354e94f684f5a33e60db694b17d89eb5ff42762fd85d2c7ef1d4abdcb2af6c48700f"
                            },
                            {
                                "filesize": 28853223,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "398a11c7c34d0ab5f0abec056b6b032ee8ddbb5a7572c13c1120cb1d16c58e140a477b1a07c0bc7f21fe087562a4f65be1ee2776024e3e03b86a6fd41c04e4cc"
                            },
                            {
                                "filesize": 31301907,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "d6d2d7de2fae7958a7baf651f78431a4eb728147c5109a6865452bcf3e79edc87965526679d1516797d8618670f0475ab1379dbfc94acd96fa1b2b9cfd579f94"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "it": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53099851,
                                "from": "*",
                                "hashValue": "9c49e0a73895ed88be59fac8898ecabc4739f829fdcae10d3910aebd9071be9c8ee13f4c60c110dd8755fbf9ec6fbe66b6b4c022e2d8ec286dbf11f53c0f7eba"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 3438448,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "b730ce68178de8934d2631f6df3491a557fb54f7de4a365580319597420e37ef917408c5e620a08456eb30c532bf190631fdc82bd948107642607baec99e4e6c"
                            },
                            {
                                "filesize": 28807256,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "5f14852385a23140eb469911098bd758e32d275aedf133c7b8209f4c4cba236423a09e5e1639f01da8b9cd2b90fa79e5573b9543d8b01c1c92e7b8d27468b7d6"
                            },
                            {
                                "filesize": 31230465,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "0269519514a58712fdc00b83213d5e042857ecbd0169b17c4be42d3daee52763d8c94ef28495279287205b84969fea920679472ebd7d09c70ffe46b0a387a56e"
                            },
                            {
                                "filesize": 22729903,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "9fd0bb30942641ac8b417890b55617cd8e5cc5fadc6eb4fbc5957944628326fba11c5f23be578888adbc6ce900c1aab55287728f4cf9319d8e098c84440dda37"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "ja": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53463323,
                                "from": "*",
                                "hashValue": "e33dc20831ab15ed82a72db0d7dded85ca9ef3e537279f6d0d71b88f57a275a0d0a2b541cc920de5454ce1a66ede31d36471a09e995aae2328a6985a802c094c"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 22777716,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "2a7f0c33921c555852d63c1c7189b81009372937866df8363fae7bc1e3a420ecccf5a59a1ab8752f89cc9630cb3274f4cad877aff9fbc761cc288818153c81ff"
                            },
                            {
                                "filesize": 31306086,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "bf93db29fa286d3ce0b0921ee95564de563dfeb7132e2ac6192d301460e532d2f33b040be49c43245aaf720834654dc92ba82717a5310f70459248870db29836"
                            },
                            {
                                "filesize": 3438405,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "6887e5ad67094c579c33a98f670ee9cd0e5233eedd60fd687c658408e566c96aeca36f277a29ae096b696de5281ce97f9e5ef93a97838f25fddfcb9a5b93d6df"
                            },
                            {
                                "filesize": 28867428,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "33bcbc04fa32020d201fe357baf732edfbb7900807e13dec27667d200cae9f94b9286f8b30e6dce790e60d7c45ac830140800699c29484ece9bc43ec8bbecadf"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "kk": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53255981,
                                "from": "*",
                                "hashValue": "a7e8ce6c08f3d3baf60b42e0840c6c6e60d922f4c7a6128d801878d6e9f8198c96af2cfd9332ee068e2c224762bcf3d4e96150ef0a8267dbc8df312f9a3723f5"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 22851544,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "ffa4be7be090ef38870f666084125570990466a29e7716a3d4c4b5519e7fe455d5e515c099c00645bee8059d708f9aa9a1ef89c014b082382d932cf652f893e1"
                            },
                            {
                                "filesize": 3438346,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "d8194f480a186279ce56523199bbe2d040539f58b917a433cfe955b57ae515a80370e961dbae60ce7f27471aa0e12ab65753de341ce77b20f20263a2e96e88f7"
                            },
                            {
                                "filesize": 31372109,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "9e4fd75b5dcad5b631e9921f69d2f59e6eace16f99dfe20d5222223682874e1104ce28a81b942e8331d05b0ef95ff0655c72e5f29a38fe80a54d8f2fc682b5cc"
                            },
                            {
                                "filesize": 28943013,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "5fd941aa2d06df941f3c4d262f709224e14ebc15386e9e792693aa35bb1d474a7c5c9995a5ca1313391bb03497a5d327c06cd62c7f0b7720304fd852533f6cdb"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "km": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53555243,
                                "from": "*",
                                "hashValue": "25d1266dbc4a14c45b9c8419eda8c6523f80c0fbdfc0568fda81a1c91d2a35f92f7218cb9d97620c3171a5d3de19f550096ecb649a2d16d7e5b28f12ebc1e0bf"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 22793601,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "7560439dee1cfbc35dec6f0992ad664f04d20886150281f560bef3623fada65bb639ef527427f04ce65beb4a714aa107042142f4c95773dd58affd2f8fa76662"
                            },
                            {
                                "filesize": 31431686,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "06656e30552a0ce27bd96203a176436fde92ca4bbea6c1f2c5e7c890f00df3cfee116911d0b54f382a59d7a57d9d9b91559c17ffd3c4ba18f7bf0772783d5c1a"
                            },
                            {
                                "filesize": 3438383,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "bb70b2fbad75374179048e4bcdc64bd94fc27e63e450f79aaa4d2e55fb891d4441e703c61e4032f0b0554cdf6327e170238ec623c8a09167e3229df795d499db"
                            },
                            {
                                "filesize": 28938414,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "3e3cfe898381c0ddcb6c4e74fdfc61babe4bf4fbd4015aecaae7b14955d1a0fa8ec9706a89f6e09a0133ef10052e8be8be617dd67d9e417afe6afdf5ce136c2b"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "kn": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53288590,
                                "from": "*",
                                "hashValue": "8c4f8b570fac6cbae2d5583194152d93c1342dfbf20e3dadc5adb960d939ee923540ed600b7555e61cb9614e38e1020fb8c686411e088a9e3bcbe871f0025664"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 31346092,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "e88a6758c468efc2900d9dc0921677d75a88c3384d010e7effb4d65de373932fb698e03c266655931a034231f00fefbd4cb77bc7d6ca49527329ed415b40f61c"
                            },
                            {
                                "filesize": 3438294,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "30875e8b0083270a10e90dfd24d2265f360fce9196304e1c2cd5993eb10ca1be91aadb24c66dc36f312c95d013ff809d033e919874d354af0eb6b02011a260aa"
                            },
                            {
                                "filesize": 28901386,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "d7579acbcb5f1baaa3af8ac6d559edda4140e65eaead629f6bf8b1b95cc637fad3e49aa7c8ed410348a4b07921ac595c934735668b2a9f5345e2fb66904c9913"
                            },
                            {
                                "filesize": 22777611,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "0392f43b5e7d7af98559023447a41f903766993674eae47bb29ec0155c206bac80c34ecd8143846a052cfbaacec2b2cdf78287fd43d2bf1178c11e699f38c99d"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "ko": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53216505,
                                "from": "*",
                                "hashValue": "84145d5766b6978f637a0302091f39acc729b81119bbbf8beab434986429348aa5612d9d4aef46cb12ced5ec23d278582af8c6a4faaab0f5056d19d985cc9e8b"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 3438317,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "1846a77c9c0d3ff62851474279faaab37eaf2e7e880c3bbcf868de6d47ec2d19c6299fe9358de8158637872a7355c64de8836a4ba20921e8126904097b752a00"
                            },
                            {
                                "filesize": 29016988,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "c0f4616fdf97edcacbccc762ef7ac80879ac0ce76a73264800a0d5cb0eeae93306bbdb58a8f5524ca959e33d7959f8c9aee02011f312c2bfd937b6967dcc2611"
                            },
                            {
                                "filesize": 22771044,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "f25d472b48e345f07263a991548e06b10197778101f3701fbb64957810fa2b17f1b1bc3d9202a8398e882188be0c2c027babfb9d788fb50a83b77225584ce6ce"
                            },
                            {
                                "filesize": 31436280,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "354a9c2db42320fc8aa44ad24563ef7fb45249712d2d5cbc06f21d9549a3f2ba8f9206e23b958aa3274349fd9e09e930bd5ccb3766f7700d0fa08e69bb76afe5"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "lij": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53370003,
                                "from": "*",
                                "hashValue": "372b682ba49526e9a75f4a5bdbc56a576eda66ae8d3698ae72e4dfb622992dc2784a68f32610af1ef78b9db16adeddb8ac97c672f901d236cb0ac2018bb91587"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 29016152,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "370f33c9184fa46b908a10fcec09f79b48df997208ff58916b1cd4d31bf292dd3e7357a933cafb4c2bd1bd8ca12f29ef4a1151e778fc1678a89271544dc64043"
                            },
                            {
                                "filesize": 22979165,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "9e80d379d44e250991d791d8d7e4748999668f758fb4d39f25f2efcae6e31677074b98f3399758a61a6b7503929e6c585eb4c2936e2af3c32839be99c014935b"
                            },
                            {
                                "filesize": 3438329,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "24b1f47d027cdd6908521559fe8ddb242d2c7f4e1a041997c588edcd71b23c6058a2563bd124e9b4d46505d856be071c16b4b8ccdfa0d0122f77713a6a1f3d1e"
                            },
                            {
                                "filesize": 31422749,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "3e98bc4e3978a726d8b97efa4aa621bfc633ba5466f3db0ee0e935038bd544e9fb8cdf3ebcb82d7359667b77d1e3e2ad1004bbe7d7e31746064067bb8eb43c03"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "lt": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53556322,
                                "from": "*",
                                "hashValue": "0fa98c6278f9047dfa254ec9ca9b5704953e3af41ac0116cc298af4bdf0da0ca6246fa3fe51385b6d64b9d402b4cb2fdfee16af8b4b3e90f6a816c4acd26d2c7"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 31352646,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "36648b230ca740f826aa51dbe34d1f8c8ecd4bf73734cb3d9c70a437cfcf4b5cfe5c1dec948ea3b142208e0c3a5cc0949c9331d667267be7832b8bde8e9642f1"
                            },
                            {
                                "filesize": 22813386,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "103e0c24cd47fda808789f7f585b10e28a1e0e47a3a5d8d9a727936c3c27f3795c0b9f0146dd34aea5c29e22349563d8520537e3574aae818f0d09741b2e9c8c"
                            },
                            {
                                "filesize": 28936988,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "d1339e9fe8c7e016ce403962eba6f764af52f68d04743c18fdbc7a20cb8f9f7091806b98e487ff4a9127ba6d624f5e4d0dab7d4573d64efc89e54c54e12db200"
                            },
                            {
                                "filesize": 3438326,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "b4be2dd6962cd4db14ca5f60bc82f4dc5c32cdf14492b22006c17f3bfac123e0e7299740bfeb37e810fd5ca0a535f9f8edf58fead120de818c18749a5becb330"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "lv": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53500190,
                                "from": "*",
                                "hashValue": "98689b66e5dcff1be57948b8ca60b7993dabd52c4503b5681ade80eea74a57a0217c751f8c2d9eea59fe6ca693633006d11bf7855f4698b2c57d01d42b0f1bf4"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 31297878,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "de24a215b6dad8d534e0e2142cffc89ccbf39b189acab1b16811077d56bd09a8e60ca1b974a95705f4b6b08893089c96a3c8e1505d29cbaf2cd08be796a1c024"
                            },
                            {
                                "filesize": 28854513,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "db9de196ff617fdda18d59bf5c50f638e96ca6507d6cba1b1ce161aed341971f8adf5748d02a17101aea8ac405e8d77061e8027344a2e49677e43f528e8ee12a"
                            },
                            {
                                "filesize": 3438485,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "b7de16decfbadff45b1b9296e3b61a9f1d81eb5c34b3b472e85ca77815399f1a6f2e203f150656d5b5fe80758266bb58beba439afb8a0232f909774c23bb78b5"
                            },
                            {
                                "filesize": 22771582,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "eab0f9c47374cb78f84c54a4ab91184d10086f1eb1c77b9f8f06d25453b991167cd7d0e297c7901805438fa632845bad15df333f89a32bd8c84460fa6d133761"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "mai": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53265769,
                                "from": "*",
                                "hashValue": "4766bd83212c368b9ee23320c970207fc433974835fb634fd8f21bdec01b7792be437caa9d288dbaa083c55e46f0bb456908ed20576efdce2a59d0a118cdda9b"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 28843664,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "0d89ef5433ffa632f351b0dc15f0d33bac06147732a4184833dcc7e4328fd0ebd72efb05dc03929ac92c71e2858f963832c3878b973cabeb7f373e2597406a59"
                            },
                            {
                                "filesize": 31292769,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "dc62e416762f899002c07a07877a4fa4a4b7bbf7014dd819630bf4a65d77e8a1954057a04b3c74f6d355129456e644edf66c9666185513789b694655ec475ed9"
                            },
                            {
                                "filesize": 22768979,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "4b646eb032a1348e752b635db3e3ffb31663dc7fbb101b6d6f5bf63739b0ae9a5e35fa76188826a4685bb667e5ef7fe0a92b703fc21eec6c1736f95c8efd25c5"
                            },
                            {
                                "filesize": 3438416,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "0c11cabdbc9dc30e44215187d32abdcf84134683a0e3cc062e78940768cb002ed01b724a7742a7431e4422a7296f9960ed87f1a4428f16d7644fd425bc5d2575"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "mk": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 54002376,
                                "from": "*",
                                "hashValue": "98e108946b78f3ea6f131a785713fd22887adf6e4241d370af1e16e6ac059e25bdf1565041871512f3a1c5c679268fc02e1c86b8464964d8f34a1317c0298add"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 28857824,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "8a606ee7f903e0a77b0ae381d74fe037d9d65369039836edf85798b47fd0cf7cbf321c421c7ce825a233f0b752c3c72c2be541af2752cbfce646d68eb5fa5f30"
                            },
                            {
                                "filesize": 31310221,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "9a2795fd6654e10dc522791cfd6db9c197f98aea87d02e66533bbe207c18200977cca9698f4f242e79cdc016b75b77fffe254610ff74e3b6f1c32dc0d1f08624"
                            },
                            {
                                "filesize": 3438480,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "fbd34d9dc1c1c40f0b232660abd3079e17f56f8925191b552fa9302e4961ddd29f826a1b8187af626b776262ae2a74f8a95deadd7a043d4a32bd4f816cf1009c"
                            },
                            {
                                "filesize": 22773762,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "9191078eb7367eba2bce085f766df4e614a05834b606c90b97ff4f299e4cda0be0194384e35462835c3a2660c7946194b567e858ca919b2f04d3f1bb803296a2"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "ml": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53278075,
                                "from": "*",
                                "hashValue": "5cd37054f9787653ddf9f5cd91f119253ba38ef6642e63d27519a789123ec49ee902a82e1863c632aabb81ad722bea3d02c3f45537ddd4f04d9b6a6aea46ac76"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 31424774,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "372d59f0294e3d9bf335070655547b68adf0c599e182dd9833c328e49551bace3ac8370a1b2353435c652f5813d561dcef2e6cb5f8a76eba13384e47bad6364c"
                            },
                            {
                                "filesize": 29013694,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "01fc54ec660e07a37a87d1bf864313e2a655cfe15be6fabe01c6335f7ec397ad78e537b8951fe2e98e2bef2789dca959b9c04c0fc9510a2597690d21433eb1ef"
                            },
                            {
                                "filesize": 22772517,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "d5f97740d59c05960d35ae88681e598ef43ff4f1aae70d742293916a54097eb9050a993b20b8a00ec59778c6a4fe8453d177f23468fcaa22e491082621ca7666"
                            },
                            {
                                "filesize": 3438422,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "447c387f2a1dcaf87b3f28096b2a97044caf783c2d62cc4743db661434ba679ad8f2aa0b32e2f2f6defcff3fd9be8a8eefea5ca9d2cb50ee93b47f7d3cbe958e"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "mr": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53267095,
                                "from": "*",
                                "hashValue": "870da57f12ff00cab2fe9b082e2c6a06aa57e9c657b4fedf83c68779822485638f288334b63bc7c737f024e8c306b1461737b0a34f82aa5c1174978d09bc40d5"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 22775467,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "f7ca8af7a1a45a05cfd3c8f2363efa5c5fad26039d029c515a5cfdb2c056a910d1fc27b6c1bb2ad646265a9dc63c37c9c082fe4253260864e94daea5c49efea4"
                            },
                            {
                                "filesize": 29005527,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "56c26a65d17a7e0aa51c845155f3c18edae6362c972ef8d3dc8e60ed80366dc64e68d6999366d991a79771d309fa9400bfbb8a54b11b3242057a9b2cf90da0bd"
                            },
                            {
                                "filesize": 3438401,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "cb17e8c0c9b02e6f18ee08b3be575fb9a0ac7724462a5533a2632b256d323ff7f78ccaf7e69b39bd19c75012f493d0aaa5c80072426b326ce7844b277c45ee87"
                            },
                            {
                                "filesize": 31414393,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "800710c9ada51a66fd12b6ad93849ed51d53b3c4eef203d3ba6e264fc90ab2ca3270c2728628f98c031974f8d6e2ef91d942c7d154a76c7f6168a9c9f57e83b7"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "ms": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53242647,
                                "from": "*",
                                "hashValue": "743a955fa8acfcc806fc060a0dbb46591a7152c2bad26b86100bc6f829ab352f75da3c7ba4a2863664c343477b3541105e3bbe597cfa1fa8262d2a0b9c1db195"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 22745783,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "98d3dd6f6e0ee023c26993eaa1f8d2d42f60165002a67f72d25eaf4457b8a3ddd1b91b7bb49ebbc0f5becd01d78e81f3a0ae8c3903ede96e9b5782d438400ee2"
                            },
                            {
                                "filesize": 31366623,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "f17fb647270dfced6a601d77c6dbe3911423386a3e14347712cf72486764ab2069b5701d5f0265ba5ae882321a3d721b5cd398af7d3cd19a2fceb4c2ed79e287"
                            },
                            {
                                "filesize": 28949113,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "e0682e47b8001ce75432ddbebe4835ab78f6e0981194ed3d5023a3bc0837fec33cb9552d72a6d590f3c6e44964b638adb0426f999fc0651820a5aeba9750b6eb"
                            },
                            {
                                "filesize": 3438428,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "4d5b0040da465aef70aa94537c7ec90fe10a05fe520decf6aa4be5b52f72dc3d5047aac0f8186281a9602edb6755947585523a3cb4d53dce48d70eeead2971c7"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "nb-NO": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53191211,
                                "from": "*",
                                "hashValue": "9348c9509ac2b5eae94166d8cdba17d71cf051e2ec9f382609d81941b2dbcfe8094c56323b93739811437db6f5ae30c6e54fbe6c6aafb24633b12653bdd0906d"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 31279315,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "60bbe3b6d068a1729e0d5ab72d66830c985de0aefa0c8979b072f1a586546ed212f5224be441308553c589d35ad6e5cb8c481a21af138fe54223306a784169b0"
                            },
                            {
                                "filesize": 28834780,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "d887c118b955f1b4a6cb1c1b81209319d31b14f9134e7bded39b8f64c4ca5acfdbb542e490ef8723b4543c95bed0f99788727f655a0e297845922b37bedff8eb"
                            },
                            {
                                "filesize": 3438432,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "e2dfc386cf6d708f7eda23c931c84b6fc5c78229c9c4dbb8cb339e80a6432b840b437e09cc9040cb05d88095a65aa5ca7391cb690a7855ab626f1775ddab93bb"
                            },
                            {
                                "filesize": 22760754,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "b49b16ec604012fe92a5290de11df2cad8d1a901c40bc9636219dc48f45263e8ccb05076911ea3959a43df7047c863d60f8d724a4f3c809dce65f57980cf6a66"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "nl": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53957131,
                                "from": "*",
                                "hashValue": "4c21a413b70290e638e1e5b4edf72a04428936d141541249abb410e5b02f8393096539a9712e8454f1ece17f0966999942436a3a0888e3b823b7b849095eccaa"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 31292646,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "d1b65e0d9b2fe3da4f57dcfd4925244c748e2125c9778f198734b2951a0f37fb8ce28359087bcc44e89a4155fa60237cfe3d6f9f838bcb4f5772ec8fa3d2fde4"
                            },
                            {
                                "filesize": 28849539,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "5b59ce39d533b15d918d0bfc0993f7bec039bff2df4b4635ac1350186e3343f34e841cddbd809877fae3971bb214b834d761053113da7806ced772463eec836e"
                            },
                            {
                                "filesize": 3438459,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "effcdf234ca6d840d54acd648ae6cfa6d0014d4c3defdb369388cac69e0974e39b19a67eb674f4fd23624f5e3dbd41179aff89725dd7fd50826cf7db2a2ba589"
                            },
                            {
                                "filesize": 22777242,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "28a10cb33406d742e6f989ba0f5e6a51f5c3025e2c3da7d09a36df6f0995dad44b483168687cd7ab3ec38d13c88da082691115804ebd27c61d948366665dee97"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "nn-NO": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53185446,
                                "from": "*",
                                "hashValue": "2154afa9117cfe492e605606af4ea99c5e916afd81abdfc0176a7a6a3dd946e01339606ddf6e13421e7f2c9d07874048d812f30b27dae9dc104c417fca44ea35"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 28879926,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "fcd6b67300ed12931631148c1502437e990fa33de8b5654e6e7c23902df2952ed8dbaa3d476e5ab2a0b226f33b5666a3da45c5ad5afbd265fe040081bd049ead"
                            },
                            {
                                "filesize": 31291047,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "796bf693e1740408b7c138a6cf184fb90b2b7107d4f1827d82c195786304bfaa16ec4bfc6ba0681378f53d0cbd45c0d4467b52c77f6899487ca4786f4e920aec"
                            },
                            {
                                "filesize": 3438377,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "65ea6274c8d134dac3f0798f0a87fc48db95cd7a238198700715eec21b665de7b2c8440fec810b43ef7c558c05279f9020b080941b013a96a2e9f1d77dbe1e15"
                            },
                            {
                                "filesize": 22761502,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "2269a15e40278659e1060fc31afb733237f84a6a255786ac5260f27b629a434959c00562f08a6a5d30d52cc4dad357c034dc578fe3c07be5d6dd9d60107f50e3"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "or": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53506869,
                                "from": "*",
                                "hashValue": "83db018abca9da7eb35747f8d8753f64860fbcfc8df0cf2f1832cc1cbda20c6e08c9acfccbca50ec917d8f1bdb05c166bb5acff2198ba5be431464b7e9bb20f4"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 31301646,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "2854f635fe022d1951225ca3f1fe583ee310141bea329cb2dafe2a8fe214a1ce9d06d55678377b524da0d6c80a079ec4efd7c14ef9a2e848baf905c3db5bca78"
                            },
                            {
                                "filesize": 28855217,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "ae91e4ef299ada86e99e4ee6fa67ff815bdb1a78a703492396dfe9fb59f9dd494a3e7cf9157c0eae978f57b73a77dd39d3a9d78b51711edb92b55d240c2e78f6"
                            },
                            {
                                "filesize": 22774369,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "42b8c543e4a0d6a140e278d7d0a8481c39b22545d0b1f457bd1547dd6c8dce4c4c30d568cd6483d77926c140ba80b32990dc9a76061a7e116aa58d6a9ada4abd"
                            },
                            {
                                "filesize": 3438467,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "5ebbc21ed6bf0e41fc09c4b47d9f627412e7c8fb527509ee6d9bde3d59aeddb5f44980183868d4e9d8d6809268d1aca6597a6b27509de25bb0d697552793c78b"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "pa-IN": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53248154,
                                "from": "*",
                                "hashValue": "2d2ef95caa09fc17f3ef66b979dfda334cb3b3c4abd886343da0f0c93b6266d521c1adae57411bffdf3de37db5b3fe12582dea6787177ff664a9d23efc6bd484"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 28845834,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "d1866898fdc17635ba3c955804ef6df00eea3bb244eff5234eb1aac37e66cede9d29ef5c04ed12040df4c302b002d00f32e4e1f24c3b5e0aa5c4a2bec9c136c2"
                            },
                            {
                                "filesize": 31287983,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "f6b6ead78e6de60678f4b8cf34a90eb5e1cb30824f13692ad5aea371a40cffd03fa6f7fea246cd8c4c62967f064276cc1d6204ae5f4eb79c6e68db70103d824b"
                            },
                            {
                                "filesize": 3438426,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "1f1c42a266cc52e4101faacc9b1c9f9e8f529fdbd0eb355a29b36ce9f85ce2b07ea03152cc0562278786fcea9b2717c215cace99d23d80358b42e605821e1dda"
                            },
                            {
                                "filesize": 22772454,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "5ddeb02c58927f1ce4c358e05c36e718bae9b1b2f8b453d101bbb2c63eea5c8510766af61b3b1d62a03e6792c3154dfda04b5dd7f80dc6b8f67d8ae9f26a3407"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "pl": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 54265762,
                                "from": "*",
                                "hashValue": "627a5aaf4d9122ac6787f89250f0b04b835c7a4e499d14b8e872427bc3389fe9d2c72b00fd7bf023fcd1798955d97545389a29765905691af6209b9824b3d25d"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 3438438,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "e132cd51811aa2f5588d7775bd114639f10ab29209431cb3a8f17259235f71fcbfe8540ed033102cb815efe6f39e8a125671c52221b1c7fbe3d4b54da0ee3c11"
                            },
                            {
                                "filesize": 31255443,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "85a695b88dd7877b40474c60da518e160b8579b70ecd8b7ea15bbf6177cc538e0804b14b3426b83e853bd5fa95a1dc2229da4ab92e47cd11fb7901251453a735"
                            },
                            {
                                "filesize": 28820674,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "208d18f6896f9d458c6212ee5fdc01669e29cb9b990797a15f74c2c5e4968cf331b789308856541fed2f0253e6a60ef7b81c9d5febcb32bf7b6e20c3e2dc7fc3"
                            },
                            {
                                "filesize": 22741971,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "e12fedfdae8681f0273a32a54c9f65b0ebba00081026795f077a4c274b1a4af6cf7e9fd1ad32d7895b966543a524bd79c7db3971a327a893ad61d1fe28bd5052"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "pt-BR": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53387808,
                                "from": "*",
                                "hashValue": "36f834d8d4150a5204f6268360d25c5412bd9cc5c23cfecd90e0ffe39d4adcf5a3a9f03ab7065432ec08f7af968a5bbdf761308e367300adb4d3fd2aa5ff7498"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 28863774,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "83a9073af6fca1da501588e5be5331618d44768a3b50f631d739ff055d32726d714bee57a57561aaa29374ed871e61d654ac6bb38261905f19328292f6014498"
                            },
                            {
                                "filesize": 22757514,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "5edb302efb676d27dcf4be08904050ab0d9f68e8bfcc9a10de771bb7e7fc01e0f6d8010c19ff40d3bae1ae175e7c26da7e30dc3049fa2f4501f2e8041b222c59"
                            },
                            {
                                "filesize": 31363787,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "7ae180edc54007c6f535eb5c6c05aa2a150c227e751e950cf3f4c1dac295d412e7121ce8f7f349934ea2528051cde34497754534d8cc2423995cecd39f94deff"
                            },
                            {
                                "filesize": 3438410,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "8d3a3a16f0042a4919a1bd66666b9c5a7a9b050b37ad89672688606021184e9f658c773cc2f78131e29bda98a9d1cd28e4db2fd17afd051ba439e7140cbdc508"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "pt-PT": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53379406,
                                "from": "*",
                                "hashValue": "6b3f21ff2ecaed45ff4970230197a195ceae0c207f6c58bf1b7ba7321f7112c9828ea3649311d38c0e5edabc2d16decd239758a97d4ba9689f1bbe3438895318"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 22848674,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "58392ef5added868b59b5b5029a5b24b19be1839033d1408a1a5fdc289c900ac743e9731c23fd071c2091ae018f5c67c37069209d9cb9ccfb2e8e91cda185f50"
                            },
                            {
                                "filesize": 31404701,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "caa7d05ae6d7aaf180836a8843c0d9957fb8c8a8c2a1e4d0aab3d7a627b550233b160e457be77377e30e70ac9934e43a5f697d539d2c3b3e48e89f2d2942def8"
                            },
                            {
                                "filesize": 3438426,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "5998f73248a9b6066ba128a0d93393181356a6ace1886bb9a9e0d83b0fa8334906455e9b58e38c373587c492eb48d151d16d9de0d0306364d05974838ce10599"
                            },
                            {
                                "filesize": 28947230,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "79f5bed68f5f6d53cb1316f4384f9e6729ef4be0f001926318eb9fa83b9b76103ca4cd1dfc561f28bb1f74dbc11b73d836cfc83fa6065d97392edbd9f2e5da7c"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "rm": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53196694,
                                "from": "*",
                                "hashValue": "a7300ba6f8fb18e0f3d43fff4615a2fbbff2639ab6aef2044d1006fad56427693e137fe440faba57271740b524e5b208130e733c4636fad5dee106f2505160ac"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 28947680,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "46954bfb6490426b1ce8f8e36440f669395da02e00fbe00b35c3b73e0366c0ca6543de6dd6f974caf6aad32c2a11592fef332e6072c17085a189a6dfd70191d9"
                            },
                            {
                                "filesize": 3438386,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "0d40f21f8911e1307ec831fecc6b3da55d6ab71278df95e04ac3a0d52355f0c8614d7fc70c199cdc59741584f01b4e1025a59c70a3d8d7250930fdceacec2c42"
                            },
                            {
                                "filesize": 31353616,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "9c8815e1644d5af8ed073fd6f2de704fd7b092a307d9a566f8cfa2d4d02861cd42fafb1c691ffbaf6c933c025dc474afde82bcc548e1d4a4383d24d9a16f9250"
                            },
                            {
                                "filesize": 22758603,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "6a188df87b81857ef92a5de2ba85ada83af940344ecd0ecac09b79d8ad4c1b3261fec44b75dd28f678820aec343e3f2e1e4a6a79e994dcf5dbc20a4137ac8737"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "ro": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53882743,
                                "from": "*",
                                "hashValue": "529f28c2af9cd13bf60adf9919bd1af9615f1cb421684bf36de863870a0d3269b6c42388d660ada4b82227059070825a55d4d5324c2fe6422a184ceaf082070a"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 22784323,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "db18f56c6ac9f9986627d749e310b1fee95a4fc38e37bef779924c50a44ec4c848a5a48d47b44e6548f987164e52d6764c4f5b7f28143456fca0041c8357781b"
                            },
                            {
                                "filesize": 3438418,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "bf225a87e800050ef74e2ca0db45c175714cafc68de53ddced363cb781c0286864a029291b2059491426f749825351471a99fb142b20673f9a070a8b2a98f2b2"
                            },
                            {
                                "filesize": 31426884,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "e1327b353c85474f209d9a7e7af1e36548006668da1bbb1b9fd7aeeb83fab6959cecaba21d556f485fb88dd0912f00a1a5626fa392ac90ff028a4cf0acbb6080"
                            },
                            {
                                "filesize": 29007587,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "140baba4988fc0d3fc8ff791e75328834f30f5d447ba9a459a3903a0f2fa15d2f7944513764e332e34e23f22e60aeb9d58a612c157b9faacfb88624dd7a18af9"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "ru": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53677635,
                                "from": "*",
                                "hashValue": "175e611cbaf9a37442df0781471445629704292ca82b698b37a3c10de5ff2cac91b22c86856e1988e6fcadfa1b4c212ede5c4a5945af64a43ea6382aa00978cb"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 31253895,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "1d9fbfb8a5b1a2a3f346f369ebfc1e0708116f5e176b8e2af05938be5f14b85a7966fa5c5350ab31d2b55c11d46c5ac8be513de13764b5b2ba07c45a3ba677fa"
                            },
                            {
                                "filesize": 28820127,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "a2b796b0ef618132576f46040342b5e952eab5a5c33ac1fb82375dbaf5ba3955472b169cb6f4cc293c4c67d4b5e288093e9511c8e52e3f703ff8e2afeba88d7f"
                            },
                            {
                                "filesize": 22744632,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "4f6ef1aa517378eaf51b0ef0e3ebc48678ea69781608c7a24841de07747950bf64b57c641a7019f935b5fb6c4d7a4d90121f72f1041da886e25352b3f82ef0e1"
                            },
                            {
                                "filesize": 3438300,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "152b5dd72c2764ddb361e54daaed4ea42521aef2ca3a68b5750378e42d8198e42a4fc5e818508c36b4ff10961cd0be5323a4d287328d06335e10dc6cfc68e250"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "si": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53288272,
                                "from": "*",
                                "hashValue": "099410528fac6c1849a8fb043e9a25caa2018aac35248878ab37fd43847b185a9bcb492d4036e421addf1c466cd388557be578e88e8ae669f36ec07b42bce671"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 22777712,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "e9bf12d2a91fea3eb077b3bcaf5b1d75139a2efa1dcdd26964a5c1249ec921d0bae0d012e862b264c5df8d7bde1baa741bf1b750e246dfda06684267453270fe"
                            },
                            {
                                "filesize": 31436432,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "cb4a861fe325d8b8967d95afb4ec5b52106bd897964913d2e64305f4961b436c4e5d8c5feaac7735fb9f66ab4944eab209f25a6ee8a717b4c7b52afbe3d1fe93"
                            },
                            {
                                "filesize": 29018320,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "9981811b9df94197395ebebb9fbb0fcdcbc74c4e4acf02d2a206ab9f02c4621a6232dc2fdbe614718c46b34484e0b1ad4bc3e2a9e534cd96dc173d51c8e4c7a3"
                            },
                            {
                                "filesize": 3438276,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "9dd9cf89a12bc895038a91d9eb3eb5af759c445b63514ff83c0965d6de21e8381a3290e47f24268f2e8b26fdc53af3218c18606f58c2c46d563eb78a1f5fa66e"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "sk": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 54116603,
                                "from": "*",
                                "hashValue": "e4db03308f3bc1e50cb7f84095c9f3801fe6d014fd66c5c3ae89b94c3ffd342f5bf05e29d8f419613ebad780d97f780137af63d0e3d852c218bc96ac97a89cf1"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 31291306,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "9377420cfa50b2892862a2bf8c2bda543da3716f1f355536b4638cdb692fe950da48573c656d1922128253fe08a51efb8b677406656adb92731101f9330555e2"
                            },
                            {
                                "filesize": 28843983,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "fb8b85cb87594912243b90f0783792f43ebc8938ab495b559369aed45bf3db5e0a920739a431375d4a2c505a0068596c705d6e59f97268a496d08863ab1ef25d"
                            },
                            {
                                "filesize": 3438463,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "260aa9bdc339e13bc8c0f1725b57d0324958c687bee2adc37a5633bc391afa5117ad1d0540c27b42c5e632e3d52995d0185cfbe7d6ffdc919fd9790a94af8f7d"
                            },
                            {
                                "filesize": 22774940,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "b7295972894bb58bbacdedf152a872cd7c329e3c4ad1134c951c6d7c4269b0323dd417f312171273ee8b2cc6b244442f9ba983abf0005785c0a3c030e04ea21f"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "sl": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53189136,
                                "from": "*",
                                "hashValue": "d3a5cface10075763be05b02b6dafe5bedd90e4a19a40850b01d46e876ca1c145b9916db004ea8b53251c0ff717538636703b33fcb8461bb955f8a8bd32fdf28"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 22765016,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "fb43be2a3ee76ed2399bde925abfacc9a91d124df1e6f16ff1c22691fb48af000f3e0a6e9fc442be450813f6692fac48a4a53f317a4eddc3045c6960bb0cd06a"
                            },
                            {
                                "filesize": 3438411,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "13e17367058190441675c25c5598848c3810abb73a63b5bd76a5a3200225f690e75043fadd5dce0db17883275f9ff995881fc9476b5ffe7146d68d25173ec69c"
                            },
                            {
                                "filesize": 31290621,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "526afe6946e5d0df468c7d0e0486f0785ffb76cbdb7da75c0696acb3a9f96efcccf3d30a9a6fc473d5aed3386b14e767771fdee802b9a5edbaf85bc0f65f1290"
                            },
                            {
                                "filesize": 28848223,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "cbdc3bbaa7a8689c6da71cac8c9142edc0d935388bf74a44265f1f3689323b8219153bb7a902e3e27de2134d28d9f8dae98e1549da9959c96974eda0dd442d52"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "son": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53195495,
                                "from": "*",
                                "hashValue": "946920843e3e4398437f0a926060bea4fd0bc398c0a0766d8c0cc128595f8721f77a49c1782c8d94166731703485a3ad6721e249615e391006a344ac49407701"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 28888469,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "6a7e4914fa64e6b5a14dd2cfbaef51f76f9afe47269a4adc8e440118c636ed89d387ac041dc54a2cb65c9dd6aee570231f9328f659298795340e09cfab067701"
                            },
                            {
                                "filesize": 22758450,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "b59340789a63ac41dfb71dd464e05361664231cd26492df20a44684644fe614e9fefd548365b4ff6f5d73f48f79a07f2bc11d3fea55d66d2da8263a23ea8ee0b"
                            },
                            {
                                "filesize": 31325011,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "a187c9dd2ef6f1d40c9711e7db3ecedefd8000e9206dea7a55ed0cf112054b0667b20ae0ff47171fadda500935af5d0f5a4062a2c1376aa68619a2d54b514d85"
                            },
                            {
                                "filesize": 3438384,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "4f9330002471d9851da6e0100f6d3aa286e11fcae3dfad1cb68f7773eaf2c070e95fd0b07c660361ee28afd9530756fa62e6889a3de63ca16c6dfffcdeb6e1c2"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "sq": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53234547,
                                "from": "*",
                                "hashValue": "f8a0545ebc15c0a3a0e04a948b58944d1f08c0076bf5f98e92995d98b5559005e349370fc2f28e27e162c20a8f3e3bde0dff801a076e51db9851cdd457a0e7a7"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 28908324,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "ab71534afe27437c261dabaf34d042bf05670c671034f0f3f385dbda30950165e5060d1add8e671619fd30623e0447ee26f9728731459bc8985ebbbd2deb9acf"
                            },
                            {
                                "filesize": 31327757,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "50c0953c286021725ac59e644019d31db7d02b7228c3502baf93035ad60e9475bbc166ec47a3215f360f3ed30d49da14c31753659f5f3db7f8eaa860223a957a"
                            },
                            {
                                "filesize": 3438333,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "04e661650df24cf48ceb979d8f068ad2aa3bed702606e18e37bad0feaa253366de93a17e0aece8d14672474023c33b5ce2b452795fafc22a2b3c40024a1f317f"
                            },
                            {
                                "filesize": 22777495,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "04d3f7d2be28a58caab5370aa8753dcc315ab7b86ee56561d55ac2e426e3f2ec1e9b54a9ae043769a21b4e94f3b8ebdf3343fc9f4791c8a9907b469d6f27f5b7"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "sr": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 55128100,
                                "from": "*",
                                "hashValue": "59b9762dfd6ce905fd8762bc8e6f852da5af769d837997f86d0a20a13018d6a748f0f4d2e204a041db5531ea307cee06988562d10ce7b0673a450e3f2d597913"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 22769753,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "67f44be4fa9d49513415efaa62035e6f454dfad5fdee10550c293d2bcadec909d04142cd2d564c0b3a0c75ae6595f1b72866447985aad910a885de5d3ac4251f"
                            },
                            {
                                "filesize": 3438327,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "25ab5c8462061c0b7b5f2cd002cecab9d4ae3fa5ce147d8abff67bfa17f06ee0754acf1adec816c722bc5d41d4f22a01037c6ce6c09a2eec5385aafd157ce694"
                            },
                            {
                                "filesize": 31393288,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "61c9e81d51e337924d9ef325f886a0b95c563262dbe95f4bad5c6bbb57a5fbaa76cfeeb08ba7abadac7ffee62793f8c99c92b34c3767db39506dcb6cc1ff808c"
                            },
                            {
                                "filesize": 28961146,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "8015ce319de328c3a9783bab93566c0e804bd865646f0739d5991007b25cad20a176a4c57465f058a63da4377b9eee165b150937bca565b9f74870231a8276c3"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "sv-SE": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53824147,
                                "from": "*",
                                "hashValue": "3282b7401989138fd0253da6bcab8d6463fde7f1d365236cd93ac0aa7655d2ae88ea12c296dec15ae9c593e71693ff6918d502de79bd0d481dbefd3a45d14438"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 31297725,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "99965029a23570f7e3484b6bdd9b9aa72a04bb9d1730b3f3fe461066c15736efb894700f47329bbbee6634f77b5ec0d8a009ec8eff68108825d8e00341cd4f26"
                            },
                            {
                                "filesize": 22756110,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "36290f924565c15ace30979021f581023b160ed40bacfc2811c76f061ed5d11d14e81aca487d6e01423eff9238b44dabd776892459886216931a168f1920f0fc"
                            },
                            {
                                "filesize": 28857008,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "90d5ea6a1d1e26b3d2406ffe389214adc79e36023fb314d9f03269a4f928a5593a0001b065ad38f6ae5e7589484977ab2543e43428a1f2710d20b79e16f31983"
                            },
                            {
                                "filesize": 3438327,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "4e96f6acbd2fb9b2448589c0c4df1cf907467acfc4175f43261804d6508b2e7c9f5a12f021c7d751a01837f08c5a2ebf8705c3bc6fd83f368c7cc1c6aaef7284"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "ta": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53514009,
                                "from": "*",
                                "hashValue": "9c3aedd2d6b4ef81ff8ca0f89836859d707647b4bdb9afeb252573bb3829d658c9531280f548995a69875fe66682acf8b384d06e27d9fa549ac108bac9018ce8"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 28845199,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "cd8e74348de79a1ecf075891a72a434e5a14b5930d7a85fb1693b4e70d76467d8a9caae432c3a84bc6519c8fbeed6df16c77cd830d88f75d85d2a15620c0c35a"
                            },
                            {
                                "filesize": 3438343,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "a74f6f53c2dc4a32662d901e3771478454b8f52c3c8fda93338c35004efed089034c8aec8f05482049843ed69db64e66935a44276afd26f8bc5da346002ebe6e"
                            },
                            {
                                "filesize": 22768017,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "85be188c46ae783720c3e0b50aa122f3097d9a8a1fddd66b032466a6cd1afd1f4bb9bdb9609a672c288b77fa1f94f33e83a715120677e24ae3f62cda776bc7e2"
                            },
                            {
                                "filesize": 31307774,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "373a7a3e05849231ad335f0c06e56d49df21bdee08c8ff4414296be3aeea91d14eccf485e997946ea9d5442f300732e5f3f0f6076fc71a4865dd036eae598fc6"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "te": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53277810,
                                "from": "*",
                                "hashValue": "8899d096faf2a8bb659abcdad98b80e78c46584b414afefcec713514cafa872852251e0957475ac07b2c0c5d24cb747148d4318ac0282caf3a7cd535ce160f7e"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 22754111,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "3b6da18047fa24828dea0597293306e130227ece2af47b11d54ef962e4c075c9b299a1277576082f8ce5d2a16d9999d88b3714ea84757a5c4474cc964d174743"
                            },
                            {
                                "filesize": 31372930,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "45aeb107fd877e4d2e654c7430768ff1e805a510d67ff9a5e76326c5954b9ac3f659d94e4efa050d03817a02f4feb7d441074be6bf50bae1c9f891c073e9be43"
                            },
                            {
                                "filesize": 28961244,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "36ab87f00ffff403064a9597303062fc6195a826ccee58f661d5b65ed6d66f23215b081e73f966f32bda9592d61b67bf79e926865972c9abb932eb67d996cdbb"
                            },
                            {
                                "filesize": 3438327,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "5eab21f695fdaa4bc169c476787449fbf96e4e3bdfb917f8b6e99f7cbedef590150a94bdc736acdb6a9314f24f2685ac8d5c07d3cd8251ce7d47e3895b1ae0e3"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "th": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53286228,
                                "from": "*",
                                "hashValue": "c33ab94176def817c82989cbeab9991cfba6e60db61c27db5c800e2197d4be6ac0012407fccb52fd81397ca9853e3843741f1876406ade349c161824eafa7b27"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 22768289,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "b013140582071d4f3b95d3b323db4ec9c9893ddc301f9edf7b08e0202cc1bdb819f71f981759af29e467f4cb3d2a5f77beecc5af95e25c5a403dd96b536f3caa"
                            },
                            {
                                "filesize": 3438406,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "662d82f7a031b356c15a0ef0bc3bf3e65b0fec90bf5cfe2e2ff46f16fa727a958315500dda3672f0a7a42bc10acf3c0973011ba053a976ed85539da862cffa62"
                            },
                            {
                                "filesize": 28953993,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "16e26fea4d28e0400d7fd48d154fe4011f541bb827bb75493394935348c8498c3d1cec26d4a0d6d6d55f73255e25f7c05ca8f84cd8d85f32aba864349b3d0a1e"
                            },
                            {
                                "filesize": 31371559,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "92fdb70f1e58ef52db4ea45178ad5f16e338c6b4e9c60e2b56bfdfb6e4976ad01b918dfc653ab009bc2399e9a8b32c5d34cb42c118e022cc0a550e0e587048c3"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "tr": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53231134,
                                "from": "*",
                                "hashValue": "adccfec8894258f9016772a9ea2d68b9ea46b700d48425e04fcb6c8bb1eaa41bdb2494baecdedaf7e78f978e77bdd631fe7e853fd5b184cf59c8269f12487475"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 3438427,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "833fa601ef99645132bc792bf1f4c913168654909e7e90821705d819f08479d009f69ea526d8443d9261ad60c7770ff984c74cdf4e6a79434ddae0d9629b50b6"
                            },
                            {
                                "filesize": 28898430,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "ec7ea9c030f73987a796bcb4992234b3093cec014a7250db2035335e1d4f325fce47b4d6502ac40c0e808e859382c3c9dafc3102efc1c04b253353a9dd0039f4"
                            },
                            {
                                "filesize": 22793355,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "74070e9df9594081821e0d749aefdf0be506c6f87b5d17bd81f34a8b05f8510718448e6ac7029f6ce99021b1e3e8617d2c808641ffeca9277c15e22c55f8b31c"
                            },
                            {
                                "filesize": 31338872,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "3c638e6081514905df2131aaaa0bb089817ad7a30c89b7b3356d7bb4b305dd8cb67f30a1a64424c1b571b2bb08ab15e6572dafcc6e49dab0927bba1050de7276"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "uk": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53675222,
                                "from": "*",
                                "hashValue": "fff553bd66d7b8e570ca0cebfd0431f000e694ee9c24d2ed537fa5e5f029640a72ad19530cd8aab43a53fcae780e3884401882ea6141fa09df7ae09265763331"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 28885705,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "88b74d5d5e6ac188659ccafc6803a300bfe1a43bfbfdd49b9a97d4c1e2d6a3d0726342db2d760809f3b74c43e6e038075ed8081012f7eb6287f80ed56b07d503"
                            },
                            {
                                "filesize": 3438596,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "0acf79148400a2998d2bc815f73ef710405634b09ed3f1eaaaddc3ffb7c6881a477e2eddb7386e21d304030a28ac2f7a8bea745d9d1f16b1aa83725b1896c21d"
                            },
                            {
                                "filesize": 31344764,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "0001a1e68224980b4b168e7a2c3c754a5038c23902b10efe7b8d086fbfa377e8f2b457192b81ed4738e93b153234f588b193bf4b328e6b5003eef5d7c1d8542e"
                            },
                            {
                                "filesize": 22797136,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "0c891a4314d9baa276cce8fdf6a30ae45b1a97fa10b0a8912bc7ddd9f496786ac7b32fa49d48b33ee5522a4d880595708717152426f92af2e133cb647ab340fa"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "uz": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53246840,
                                "from": "*",
                                "hashValue": "496f191e51d1903f30e6e49f763a1861b573de72c4c36572eeb87998413ff874f1a70fea0442e32a53ca38d01d25883549d6f7b8b2649f0a3b19a34a53a414d6"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 22746998,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "1f64f35f0d94236b992f44d191eb96cf959399ed8d10f6724093a63f147516e3c4789f71bfdc8fbd5304b0bcfe7958b512ebc9624fdfed5295ccc7ea7daa8132"
                            },
                            {
                                "filesize": 28927608,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "78695643b843abf67b5e28b2b1efa875276171225170bdc6e0a718f233ff409ccd8197c7f6918db532321be50f8bc4fac31c7aed3257d85a4872c4d799cf1fda"
                            },
                            {
                                "filesize": 3438594,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "e760a7491a277ec86c146fadd492905d6172d34fbd2ebaa00482772f5fb43f24469e3e54283be861bd70b0d87059d9537befa8fad93d15cac26de2c9222ec441"
                            },
                            {
                                "filesize": 31346548,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "c6e0067fb05641e4ecf685f732eb9afc8c0c0998177d9d8f826d173117110548a5ff40a0bd520ee54b99177cdb7b2bf4d9edd7f9d60f1980a3d5d2bff9bcca7e"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "vi": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53244081,
                                "from": "*",
                                "hashValue": "3c11ef2c0bb205cce0a4178aeb98509207cfa19a7b3cd3673f3d77b34d2fca7f414692ed33b357d8ccaf50e211f9dc53b13c80fb146613fba8872be7fcc7f49e"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 31341938,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "b0e5a848b27ada962d7a22d72a68c15cd5dbf1cc5bb4327a533e973213c337506882a9b6035b1604c654ca9b9d7aff7aba08c7522e85d457d330596099c432f6"
                            },
                            {
                                "filesize": 28928925,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "57b35d943aef836a8f1248d6d21a4965175b72dd23cfc45f6d7029dbf5abc265ecb94ec0756fc84597c7d56d70fb372db49d38029f8b157df03a890c3394c252"
                            },
                            {
                                "filesize": 22764687,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "0cae537edf57992bf9ab74b4fd8486482abd6dad197f0190eaf248f05f837eb86765627da0bf5b8e5e01ca31784276eeb5bbaba8c292e7026957b047565e90f4"
                            },
                            {
                                "filesize": 3438673,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "0428406f78a6dc4dbd57d763575f56102f6d5119238a1dd5cd9c5139ba7ca832d883dc3b1a154ca6c875f85c71fa7a4b3fbe9b8c7975ea3e63a7fe00a14b2384"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "xh": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53195952,
                                "from": "*",
                                "hashValue": "3ca444e6c968c17ff424fd9b9d52648be231f6762ae90f75f9086c042094b1ca9afcc1c1ed12a908161932eb856a8f11629e1c184cfa345d3aabdc0bcf89ca36"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 31384418,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "7d83e79037657e7a0a1b5f96e62afb6358cc141fa207c0812b56096cefa36ee5bcbb177a6e2fefb83b1d38c06020602f6de64ca4a34437ad92bcf914f0d9b8be"
                            },
                            {
                                "filesize": 28974868,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "dcbd7da0236f21cb7613712a70ef805e53b035eadadd3847a786067b5d4d07334b6221c6a7c54c1de81671cd7cbc2405aa361a1c75b37d7cd44e288240ac1c11"
                            },
                            {
                                "filesize": 3438624,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "f98089768f96711dafdac83d2b618f9c795ada5f3803483da6b3a4aa435f9360c5c971d446db9aaec27a3a18cc59666f2e722396623402a3dac80cfdace70b2e"
                            },
                            {
                                "filesize": 22810826,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "7cc6b2eb0b9b9abffe5bef8dd7986d09948afef9188880856f9e404d74fad70963f8ee8257dd3496a4d8b494b366e08b27cdfb785fcf0242679586f294c90bd2"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "zh-CN": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53229876,
                                "from": "*",
                                "hashValue": "c5ac1ca6aff24e7033f47e729eb73daeea0cd000b2d31e2f78108cd6023490a2683c7c8eba71ce3c5783c137d7a3decf4d70367937fdaabc214321113eac6cc4"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 3438547,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "5a0371ecd9223b4de4809acb17b436d2a7cbca7ac8de14018c4845323c8b50a780f3729c030b3494fbfe524cc06655d062581b2a369ad9d671a0a4f03a0f3864"
                            },
                            {
                                "filesize": 22781503,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "8aa4bb4ae864c6cd66dbb87bab4790a611bc3c7db541bd13aad27fa61a67ea117ebb920849e02982ef030f3e1ca2437c1ac8f038f74427c48e6c513f6025eeb9"
                            },
                            {
                                "filesize": 31302952,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "a341408a0f337dba5da8048e122e672bd13d24f7e200b3543a5f4c5bc872f1f9e57caa2574f3a3e72ee116fd3e232ee29ddf8876bc8f2d99ee79f5be293dbbfd"
                            },
                            {
                                "filesize": 28861239,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "e3037e6cb3907657884326740947633bc31f36b86214bdb700e51f8d14308363859a04c381846332d389f3d6cd517acc9ae5f5f77bf1512e782b6a2a9da219cd"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "zh-TW": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53447834,
                                "from": "*",
                                "hashValue": "04dbda1b89f0461d321758e13de474ee71b5310e15a1b665d7b3910bd75421f306cd330e0217d433552a9e42e4c0d1ce1eb1030991353aef16bc0b05e8ec3f82"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 22807151,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "81874d2c45c3604fd231fde8563dddc0e1c0502ead89cca801e5fea1b75bffa73fc35bad36064b653e346ffe46d8b33d4f437eaa25284931175ace5b9f0d69fb"
                            },
                            {
                                "filesize": 28880863,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "5decc21acc7e2e56536842e69cf249fb6041f5667f91f7d76c3dfb9545f0ad166ef8f2cdf058bce48039567eb162fbad9640beed101d1c650f9c1af4db2eba6a"
                            },
                            {
                                "filesize": 3438561,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "7788452e3d6394e5592fdbe784d89e6d7ba334f0053661c9369647a37e57793bc52618d798089e4bd7089491d985e1360dd767b22758aa9d7f2dd4bc8ed5cb84"
                            },
                            {
                                "filesize": 31316452,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "d4430dde3c1b2e862c4db078e6664b4f4d9fee036472d0164c43fb9c0fbc065ddac20ecd6e561e2030e64d9bf0f22d162a84e2aba920ae10753d4a37891b5589"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    }
                }
            },
            "Linux_x86_64-gcc3": {
                "OS_BOUNCER": "linux64",
                "OS_FTP": "linux-x86_64",
                "locales": {
                    "ach": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 52255950,
                                "from": "*",
                                "hashValue": "556191af3b5034fd8d1a31245098c634037b7a8b5b071753550cc4a1e7414eefc9646dfeaf3dc5ceb326d6a1037b04fc72eaaf20d2d3a090f4cb5b5d99c52f21"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 22511693,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "05f584d0d5ebdaae19346b3cb5f693516e82d4a363c3fe126674e035b7ad02949417ab96e64a51632380dbf038918dc9777e0593201347ae247c22af1157106b"
                            },
                            {
                                "filesize": 28422557,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "c647cc2b5840b8ddbde604f0fa76e0313ea324dbf075df83432fc2c759ebf1d01d6592556ccf2f84c0f16d821f926dc29b45c72c3737f569d139e20a52975773"
                            },
                            {
                                "filesize": 3008720,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "6a84865423e9379c508e757baebe7ad92285e093fe2e26842e17f87050291864630624c70b3df85f66578f8fdadb88dbfa5f1bd587afe3d2e1c3681158bfa859"
                            },
                            {
                                "filesize": 30645633,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "b4f8e7153323063ac7b5bdaa18ab235c8f06b455d7dfb3c4aa5d74afcfa068e5b3eaa933b96ce3870108d392922b97ddf8b570f89d749f2be6e77ee73a62cd10"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "af": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 52264880,
                                "from": "*",
                                "hashValue": "2d96830bae974d5a226020c4e4b351d7f5eead26e7f5b70ae6ce1013a7e86d594a3099192ebc4391e7a1b16b204a6682e4eda1166887ac30d90f57b2613c1b70"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 22463974,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "1e0fbf08f6cf3f760f2496440ee31e4441359aafc5744bbb46e0e85f6ca3f87818f5f66c310a65dc4ac6759c34199ac7825f7ee04ea1b58cb087d938587dd3bf"
                            },
                            {
                                "filesize": 3008738,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "8a47c50fe876381d129c86a2fe3f43e1806d6e2d32214cb447ff799d0bf4d20df89eb26d55147ec6f469f8da38dd1fa6c6c2afcf73735c5b62d0ccde52679b49"
                            },
                            {
                                "filesize": 28362846,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "4be0788b5a1af407a98ffdd505d3eca76ab11fa091aa1d3b0b2c70e6e895aa64131a4caf17eb2c697706487cf984495435d8c96ebca30fdb0f16ac4f8fb72a50"
                            },
                            {
                                "filesize": 30619972,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "d9fd23e1cacfc61395e8bdeeb294b44116063f5b82bf6d9c64b127102d15ef70d4be79c405930c57258cf3d4b6f6c6e665143509ecada3b8c0f491430d468eb4"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "an": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 52243688,
                                "from": "*",
                                "hashValue": "b300366201e697c2e08fa957920b40f454e7e4950a1df82867576c9de6595aad092799d12f0b479255ccdf4f2f1ffc56c8044bd766ca0818eeaad081b93fa2c4"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 22462267,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "3b33ca8f6e8a4010c1d996c12688e91f922f2894f559c2209d527eb70d6b47d310c2c4cf1009881a40a0de1241c8b4e3cb15ae90b00d0f8f620895156c836420"
                            },
                            {
                                "filesize": 30578773,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "6e0743b0abfd8adc11e1ef6af37db3f8485fdb7be6cf122d6299c7f16141db29034323bb7396b4d40d708e78e6d6bf904fb46a10c1f96582bfdaff77a94e63bd"
                            },
                            {
                                "filesize": 3008735,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "235edacfcfe70fea335dfb149e2a04c2eea9460f42bb45091045b4ce5afc96dfd2316accbc2322928c6d5938ac08582b95ee99d5ce943ff1acfcf2b9300b6c72"
                            },
                            {
                                "filesize": 28341495,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "eb493f906dd525ae436ab154e426c7fd013ac0cb32e5198a0ad7f437ed598b8e27e7f007ef3cb2921cfbb99987712918c371f9969b951929e987583d841c02d7"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "ar": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 52303259,
                                "from": "*",
                                "hashValue": "d8bc12d401f5e65f398058d0afcb458669e098b93d62149ef5187e42fb04962c8745ee70d896cdfe676a0ad748746c2d2e50ea9897157b7f14f7387c2b92a395"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 3008726,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "75061f264e60fa341f6534e254f250f30a57e1e3cf1ce466a00d89f4917395177ba60be0e4f39b24915cf39b5daac2bc62a4a6fd178fc87231a95ebc7d47ccc3"
                            },
                            {
                                "filesize": 30651310,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "a4831170a82df0bd9f2af2fb14b066f46025329fd65a299bc0fa880c6fedb7b4702570ffb03be9afcebf2bf23aa0ccc9dcae6c9c9631ba3a647036be643ed0a6"
                            },
                            {
                                "filesize": 22457754,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "39a939b977589e1dd2f95509f508227629580edd9396fdc324095b59883dd1c51ea226c72b41b8274a1b53790860336c7182ca1186d17b86e9095936d0c5a600"
                            },
                            {
                                "filesize": 28390853,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "c188fe4065fdda02f477f3b8544a2caa64881f746f6015360a1918554f16170f30dbd58b2f49ec075432a6ab5fcd005e96bfa7cb587ad33970be2ffd31a02d74"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "as": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 52292557,
                                "from": "*",
                                "hashValue": "f3cc1fcbf4478df88a773369d3cbb56d081d7ff90c3db31adf4400d534626cd53544db2c3875a4cfdaee548db1b3c5957fad3f916441e8057709f76569f8670f"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 28343476,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "7ea841d7309a655ade7198d923bbd0a46a31993992b23b763671ffd18e6e83e0357cf2077f9351624c965bc8b4042d0afc475e757f5910b1be771eea332a665e"
                            },
                            {
                                "filesize": 3008471,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "21e6d42f3e95cc74a2c630c170af413afc2ced31aae76aae8d503d67e150900b4013fa95211f87cda2fbbcc11613bd9719acd4755b6aa7d9bfc5dc670c4cecec"
                            },
                            {
                                "filesize": 22471048,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "9d25555116c59709a46c62e02913ebd600061084cc2304075eaafb17367b0984d1fec2cc99303f612b07f4ec25a581ca4fa01464b147639298ea6fec0cc20c5c"
                            },
                            {
                                "filesize": 30594545,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "9a0ba48880b0ad92d0b9edd9d82291ce1c1963393a3499cb7b98e662305d06ccd27a0319faaf993006ab0296f46e71cd87944518c8a12125699b317b962ef914"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "ast": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 52181069,
                                "from": "*",
                                "hashValue": "fe7a642f458e47f3ca63f43025ad0235c90d012768f21c9a6147fd69347e5b1fa262628511a98f2da7f6780763f07214346aaf9ef4c3b070ebbd7b256aa60b13"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 28293245,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "049bcca088b74f33642320d0fd9220005be9c0092f3e49eaf3a0da8a517cac3ef1b2416318370ea6d1531febaf285e998252fa61900f1963d7eff09d8177eb5a"
                            },
                            {
                                "filesize": 30531874,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "0a3624e7c548232b641f3af595bce898268275ff03983918e782cf4a3f816456835128ce618d5dd213449694d1c9d0fb7ddfeca5f5669a821f2d5bda22632184"
                            },
                            {
                                "filesize": 3008378,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "e60c0111cd06badfbbfa999a8e43bb984cd2eca9810e75c09369735e4f79983326da9139aeed9211a3d13c260b37c156f5bdece6a2dab5cfb62b3c0fe504d4cb"
                            },
                            {
                                "filesize": 22442851,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "80440a43f4daaf61172f9b87ddfc13b846e85b9ffb4581dee56d1e7b5ffe28591f72a20cda07aaf4b5fa24abd3331f2f703343cd61f4a21d17f023925160ce2a"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "az": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 52274903,
                                "from": "*",
                                "hashValue": "8781c5366d6ce0876a472e8a500a54c145b2cd3f5b06f81bad67dc5059e4be6d4ee34f062a4bbaf204a41bf6305cd0059601e4a9a05e9350bfdbab7b55ca55ca"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 30649743,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "2d55e232de24626921136e5c0178cee9b80529a77b2e6d35c680f82da961c06b239179e3663a0f6e252838b02dbb6dfcb7827e7e96656db3b93a572427d9253a"
                            },
                            {
                                "filesize": 3008361,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "1b63b7f2038e18fc415a1f90bc86e7a6b66d51ba4365eb51825834c27eb8cc95e4dc3d809bb8f4b24686a97febf752365da2c4f6f011b41fa796e8c27aa74f68"
                            },
                            {
                                "filesize": 22514041,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "5555324e811c8a2ebc4bc4132aa156cd8023d7c5746986142576520d66886e5bd3a003b95b9709eca7bb1b00eac2290385fdbf448f306c5e6ca1f529508cbaee"
                            },
                            {
                                "filesize": 28391206,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "d3da3007d9193c3610bcf4b27060565208d84562240b58084c28e3c3bcd89876c36d6044a69c23ceb2fde2b2f54fffa0fac7ceeb645df8048ce5dcc1165b216b"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "be": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 52231098,
                                "from": "*",
                                "hashValue": "00d3f9b0934f09030bdc46b2cdf47ddcddf1147efbfd5d3085532f95716055d38f9e9bbf146cee31c9c0ecda17549b888f553ec08d84f307ca8829cc9a9267a5"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 22451625,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "212d7609144269da8ccd2528008036bbe1a0ff08c2b8401daa1af94d4f9e63791f3174cd3eee5e5bc85ac30309a58ce55d347411d2b441a47abce3d6b6ea5391"
                            },
                            {
                                "filesize": 30567524,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "97e3a9fb502f1782b9eb74ad97662ad38e3645ba4a1adb2049504c793abf0affe38c4f651618a14fc6fdd8c72202120c89ca90e8388f8febbd943dc2d0a6000c"
                            },
                            {
                                "filesize": 3008335,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "1f6d9fa2c6c819e3bb46667b93da7ebc3287625660aad8584ba07cbc6e7e97ab5ea53832c844015e28f5f1a506ebffff7125c1220f09d17fe77ac42be1f42754"
                            },
                            {
                                "filesize": 28317371,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "98280467f72e58db28c21f21261ff755b965156a9d2edcaf7b786c560947be967aaf1303b8251e5791bdd2c18ede79ff4d9592dfbe50653486329357585a491a"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "bg": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 52543754,
                                "from": "*",
                                "hashValue": "e6b9f981bf199bc33f94cfef44a99d76ed95ae4c89a19e894282bce54feef7e70fa7e0dc8470754455f0e09f0f52346521757bfff57f4d329b5c8bad007c6b86"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 28483206,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "2b10ecd95786dfb67310cee7ff8675e9ce1f6bb6664d03f8a6f5c200ef59cf48b1a1181e38693addfba3816ad9e2d1098c5e4774663c4ed4d7f9ec22220305eb"
                            },
                            {
                                "filesize": 3008417,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "4ada6f0a6081666ecebb5a11a7969dd7173e519d2ca1e22335a37fa8381c8e92dc9860bfdd9d71258c5a64d0053526623d71447ee5611b676f5c878028be97a6"
                            },
                            {
                                "filesize": 30696341,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "af4582a9104cfce05d450341cf9fc73f2b471b92e3ef73f220244c74ba34223ecfb5d51e4cf65c70e7d3cf67276cba76dcb6027ad2e9559e1d75b58ad2ab778f"
                            },
                            {
                                "filesize": 22535710,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "2f87dbf3d910fd90212591a4f129692fecef8e76cca3043fad09053a05b8e04c6bb3c87ca7a24776565c376e98b601c5a2f7cb6e5a0e701deab24eb58b153dca"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "bn-BD": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 52322961,
                                "from": "*",
                                "hashValue": "e26e9caf73590acc5fbb9993b994771fbe0654da2a2564abcecb6882b634f6c144844928e9307ba6f9689c2f410bb6f1371252804c43c81ce0c2c3dced4f061c"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 30789392,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "5b48368d5f2ca59ddadbb658ceae1ef473420657d0b2f41b98c541226ae94aec2721ad96c672e29042fd80d0fb9eee3de58e06acce6785117b0a0f10b84ccaff"
                            },
                            {
                                "filesize": 3008701,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "8f35d95e4814065f91044d5b7a337a0b29f5a96b79846d56635f4f9b433f4ef10306378dee40d2a76b9bdcd1060dc0adc8e6068192daf8830e1e9bfd104a30fc"
                            },
                            {
                                "filesize": 28565704,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "249c4a454789853bb99ece8bbb9d41130571c6fbd7a23d6032c266d264b529b9383b9f7489bade77d81eeef6b882e11a3d62c3366fe0d09e680d8a3bd805210a"
                            },
                            {
                                "filesize": 22465955,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "9bdb59b3297bcb9b84e69bc8dd49f830cb91ad53c6f45c5806189240e2b16881a40f7049d9b21110dfde18298269e74dbbcd16eb2a85a76e48fac25ee6fbb770"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "bn-IN": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 52313617,
                                "from": "*",
                                "hashValue": "12f61cb58ed72107025e9a5031ce2bac3aef8eafc461d6e8bcfb672f697b6ba1bb4f567ef56d2920477af238e8e455342e50baaf8704912ad3ea42bc1d9ef977"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 28499506,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "df6d759c9b1309b05c332850419eb582eb9919a0c72f2810e40963e82ec20d0d38fb8a905d6f7aff4cc03f99f8c7f47867e299eae5a40fd0eca68c755bc16648"
                            },
                            {
                                "filesize": 3008707,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "8c0f9658112e9d97b77ea56468e5bf2b7750f1fc4408857ec4c243bf1a17128ac19dd2035d22ea820831e55d0779699af7c7eb60a2a65eb3b3282503e5af3ad0"
                            },
                            {
                                "filesize": 30712470,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "ac3a8406715e2b2cc9507644ac304712d1f25036689562d8fd99fd1eaff4b81ff5f0ad6fb22e0ef0ade24bdc6d89f58ce53b2781d695e9750af43d2fa182f045"
                            },
                            {
                                "filesize": 22467603,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "3984ff6531bffc3b34483d901eb7763a37e6e137ae5c90a2518571e899bbde97de09a3b97c27f5cb7acb86a1209621824b3a607800e234418850fee396cd26fc"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "br": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53589720,
                                "from": "*",
                                "hashValue": "4581fa3209a344ac99808a41623fc002f2bee46a819a0a32835c18db9f7671e476099ae9782b8cd9e8cfd623878f12357fc5d8a2e882e32db3db1b18dbf48d23"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 22452211,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "60c3104f27779057977da07536f02997d85b3d407e524eeb4735f7bed7b8b9b2cf7fe5a764f1f0f864919af8a712ccef603e95491c98ed3396b0cd9da92e7028"
                            },
                            {
                                "filesize": 3008725,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "fb9e499012cf1ba67f60f0027cdc85664f5c062110ba8a7084d7ed9e2da66e60a07c4d0271a81dce72f12165a08865ba43a27bb430b3933e0bae7d22d57bf369"
                            },
                            {
                                "filesize": 30578951,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "b985327789f8855c9bc985d2cfd138c57db88f0fc985101154243af6d302799c9459d368f1622d191baff6d7a4accbd37d8624bd4c8685369e936c7aad9ebb52"
                            },
                            {
                                "filesize": 28341402,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "8f4485327b0db3169deb98157960669554943b9cf8a2a3617de9868addcabbef8dc150877cbba701d5bb6cd199137f4e77670e4b17e03e5fab35950cbea2cdd8"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "bs": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 52264604,
                                "from": "*",
                                "hashValue": "26c3323ccbb68db391616175e1f20c16809a365a5f9429630ac05ee5acbe377867b6fbfefb2e55caf29535725a37c85e4258370da582a4605d66f4d8d5fdeb64"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 22463296,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "c7c39d8cb9d4bf004b6314654e15516160f18076312b7f3d3cdb2f24c4035e6154bbbc7b05997fbf2afcaac0ca9b319eee179fccc812d8711ca1320199d440f9"
                            },
                            {
                                "filesize": 30754327,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "9db0b12263c310432342f8c4c00929fe5c8571e9be6b4de0d80b3bc293d93181b3a4e978f2f12b5fbf8a2e8bc1c96faac45df25916b22c2aa0eb9b1df9b3edaf"
                            },
                            {
                                "filesize": 3008506,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "9a9a3ed9c501bd2c5eeda71673a3961580f87614bb35f18558f5ecee73484c44572da46c489c346a882f773a8452418981c0f941d3fa6edf962009edfde097e8"
                            },
                            {
                                "filesize": 28354823,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "a97aa970524fc37f51542a8abc3ebc0f04ede329ea687b9a5edc3161786cf5c45e4e53848c9c06046ed9ed7effe9e3f3d2fe4294a3b84ab7292df8c2c351bd67"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "ca": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 52646128,
                                "from": "*",
                                "hashValue": "d44518c3770ed146fbc0316259d53655af97bd1ebf8c0b2bbacd257b5b0c06b42fa4ef8b35618a328b6ddd4f1c5ece4e4cb339dea045ea69223081a58307b69c"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 3008529,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "dea4067642376105df8357c7c560a5a88ce10210b57d9bf2c634e48b5f4d364742ff9232d9ed0b2ff415edf422920996529f21a7a12742c8cb3385cbf7618488"
                            },
                            {
                                "filesize": 30620090,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "62fe79821bd29db3116463819a6c7fcbc5a103330f6e71c97063a002343e01c189a45b61828ca4cfaeead17e0a90f08f65fc8372352cdd8c890abfd54b215835"
                            },
                            {
                                "filesize": 28378791,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "9d8d47a607bdb94b95bb76c0deb4022e71394b74969842eed8f3b7bcceb0c136e0639162f20b46e6b8d6b159126a3ed6e639ad6a93144e42fc6c507bf4c29e66"
                            },
                            {
                                "filesize": 22489662,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "6b1f080bea134dc30910c224a8d5733d6a66c301c507eb940a4fab1c837023f419ab9d6ff6c09a4aa35f5dffb4ced7c671fe9cb706443c219988b7ea1ecac8a7"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "cs": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 52230915,
                                "from": "*",
                                "hashValue": "b1d8ed3081d2c015fd12e3fff6f19d04e9bcc49e077041f837437089ed3eafd299fefaeaa20c1fa77fabe435cee0badd161a47baf0677935dbd89827efead304"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 28359034,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "a550b580739c56c73b45afb7490455cfe8f0eaf986aeff5d8e2d9e2b38454da32254ed5216f58e5055a50ccfe44a313b01975bdddd4dc5d77847479bdd02f2dc"
                            },
                            {
                                "filesize": 30622245,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "787e369d2b83b885305ee53296ec32cbedf84f9d50cefd2b44e50a30ab6f9a361cfba0356f1b8d9e40b2c1ca4e444272c0622e047cc2e613705240328dba1dff"
                            },
                            {
                                "filesize": 3008438,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "2a7aabe2468840608c26ead9e932808533d1292c3660cff2e0d20ded29fcb776712e443f2af97d7e91ada7fb2c213084db7323160c1ff0885a402efea1b5cdd6"
                            },
                            {
                                "filesize": 22472691,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "7f8c54124044b96a18b90b2fdde5bfcffe69c94017f25a1ec4f3d1f0ca244c569d5684d249e1c91a3f7e475cbb7afeae92592d1333110b48eb6700643dc9efef"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "cy": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 52226671,
                                "from": "*",
                                "hashValue": "52346c3858100cd0ddaa29a25bd1f609fee20644d938632faf92ac96f5548804b33dd01db38ec6a43db8fb1290d5f7fda88e3b7a2af662f95a3bfee4a8e6fb24"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 22461231,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "e75598537bc005c4ea38b596e4601b7de303172b386a50af7fcb260bfae4a0f26a6370aa4dc31005d80f0791f67f75755dfb4be8a5c5ba7bdd14c22687582977"
                            },
                            {
                                "filesize": 30586862,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "8cc95be068242071be7c3c38d6f23b0c7b0ec3e60f02ceb20ce45ad8a6c14502b5b44cff0b6c52d2ffa33c011e981a3813bdd00f4698ba841015cc28b1fb9a92"
                            },
                            {
                                "filesize": 3008471,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "f5f4700f2fe9f882f6a5f8ef49ac4b3d98e3bc8dbe4ae5e85d27782508eefd5e456ac88d94def6976f335ae6a167782ed679c7f88c5c5c6636295b1b4339b553"
                            },
                            {
                                "filesize": 28339069,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "1d0d73adef9d3f7307eb04ee3c3bb511947891deaffcb5ba11313aa31991088b9a169fcce70ec7cf2944510c470ef305268bf7d8a921dc143f6558d90f72047d"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "da": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 52858289,
                                "from": "*",
                                "hashValue": "4d53645d98c138d73180c39a8e70c227a5b1204b7bd5e11a685dc52a1d1c12716b926eba7549234057838dea022aa554f6c16625d9edd1eddaef2b1d36a29335"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 3008447,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "15d00549e69db7166c33080184957bdbb5f4ecd04aa680ee613e828e3502a3a3cadadaf94f9a34573835543b3dffb82faa1a7a547aee0c9f5f24fb07485f875f"
                            },
                            {
                                "filesize": 22452774,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "ede623ea6c5a7294a0895cc858cd2e6786bb775786dc18871c96129f5e91283fef2d4815418724aa71b43e688935e4171e493349f93210034cee106099439616"
                            },
                            {
                                "filesize": 30579652,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "67884b2b4fb27391090dbc9ce0ab39d7441c7780bb215f067e416956be081e027a046e54ef9fda8f729667292013900d7928b7816a41cfb523ea504168dfac3d"
                            },
                            {
                                "filesize": 28321818,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "52cdb793889a3f951e500cb9338099d0e36763aa8c4c101a5f6e88b73460d89b1457aebc6ad6fa2a3d770a04c7f2ca54127574a994a3e5a808884acddf2042d8"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "de": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 52237858,
                                "from": "*",
                                "hashValue": "1d0246f7496f62bfeb3d14487b316b8a3135018c2a71b583ff2e3236d979d3712765b7bfadb7f368d795563d2b5fa7897fb8b10ef69ba0231a3f0eebad147625"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 22461883,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "71d73ed5ff050932aa5246e24417a36445a861dca858e014990e7be8063c5ec6ba9949baed319bb1681b72642c15aa05abb181c1683792f5ad167f1e1eebd8ab"
                            },
                            {
                                "filesize": 30584170,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "6ea7360bda907d10dee2f884b8c54c449def468e1fc09ab77684f51694d27e9360af165c18d69b8ce97186f1889d1da351454566ae8725775dc861cefdd019cd"
                            },
                            {
                                "filesize": 3008389,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "60ee69776f654ff3d9addc437d5245239fc551dcfbc17c1e9a6e05d20cb5935628bbb342a88edd50a12615b6b50a4fe4073486c010701757a13adaf8bdfaf5b1"
                            },
                            {
                                "filesize": 28338059,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "ae24cf433652ac293ab9ec9712e720f20d84aa4be299a63d4ea361b90b3725be3207baa893f156af42efe41ee260ac7dbd693edb194c96f049cd74e320d25cb2"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "dsb": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 52253817,
                                "from": "*",
                                "hashValue": "6726fafad9a96b1049a7fc7cfb284d4806d9d14dbf1bdb97d2dec42e9fc5a4c09905c9c130c04202e2826c409dfc5dbb070d33e466d4dd375efa580858801ed1"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 22467300,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "29cb08e23b4dd9c5aa18312a807a49949ad302583c5230024b1570ea97ebbb0ac85f8df427f014bc777dc85ab70c790f15e1044347333140194ac9453ee250f2"
                            },
                            {
                                "filesize": 30589962,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "a8cbe90cb87512c363568df7bc89ea3de325e21f98e15040e8f38c93ba34f9e02ca167fbe55ab5e058853115ea70c47ef15107efd472031f64cf301dd1647530"
                            },
                            {
                                "filesize": 3008712,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "14c7c4cedcbbd78d32c6ee7003cf294c7280a468d4ba083cc1f7b3b53408aa7bb14c665a24a1fb382835266e1876eef046d6e654eceb12d693aeed3e1e618c23"
                            },
                            {
                                "filesize": 28345697,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "33ef9df7bc072495dbc4032a5535779eb3e8ddb450c134620e76804a5733e58b34a1106cce07de02c7a0eef5668ff1c2146dbf5a6148648651480d6f930f8867"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "el": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 52280056,
                                "from": "*",
                                "hashValue": "c20e1685ceebdb4143099bbeeeea4d0e79c317d47a8938e90b0e6aec48c804594ad6f6ac6fb4a8dd7fc061f74700a4d80e9023ab061ea7de6d910029e7c978cf"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 3008717,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "df6ac657ec06ee77d079924cbc69766f1bb65154d5009d606608597575101d27d15b30cf12aee55e5d070f22f658bfecbd8e1a80cb6e7ef9e141a5f4f42e8a39"
                            },
                            {
                                "filesize": 28331426,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "6acce1e5f1182033efb766adf168c1dcd49e1292086f3e3e1968573cb1383f914be1c8a5e705fa030d20afde3dd8c78fd7283a989e6c6ad536ca7fdcfa3edd0c"
                            },
                            {
                                "filesize": 22458164,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "af369a41320aafa4cff54c0b1fd4557c3ca065b31fe87db96fbe1a5eaea93948fde95fe04cb80ec36e507fdda5df05ea50f3a7d1680d197309a707ef88832fab"
                            },
                            {
                                "filesize": 30590716,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "9d1027e9cfbaa319e0307b37def071ada94d9cff906348e8f6409dcf2f503971e83a81df324d2ead30cc14d7c77ee8a3253caf6c26ddf8f029a2e4db93abf05d"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "en-GB": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 52214534,
                                "from": "*",
                                "hashValue": "5a64776097b04106c23b055fed5f5196947ffb1b7be8cca72f18e0eb3b015f0016e8443b5e2579a84bb23f5ad75b19f9f11bd6514bedf0d3097dcaf14ea96cfa"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 22444580,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "794d2b4ee3a54a01202e09f5fc0e17cd665612e6dcde3c2fd9f6cd07bf5496886379fd103151f8348e5884d78a1494f846549c26cb6e68d2cea109156c31583e"
                            },
                            {
                                "filesize": 3008919,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "1940d728ce6ec67358b73007f8532dbdea7c3bf0f3449c03a83e591d6b2e379bcf4bcec2ef6019e69db7d4efbe97e6c1eb0c904b2a67b31692b98a8ba1258859"
                            },
                            {
                                "filesize": 30562636,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "3ea5ce331ad207d2caf93fbe784979c90a3710ca7e5f52bee5d77134ced54606060ae2d5b33806dd25e39747be590ff674fa7dfb80c8b9c1392b3b7e0d256e8f"
                            },
                            {
                                "filesize": 28347586,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "5f429119f587cb0971d01709b341ca3ab3a56f555943ebec9126522a590ea29d7a8b149ae647ef6dd1bf8b3fb0a9ab285f5dc1a4c6e5206032b0469f2fd6a2f8"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "en-US": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": "52492017",
                                "from": "*",
                                "hashValue": "434cfcbc053943a3d3128d77d9c1f0ba3e2aab29c03a9b5b58ca350f06413f122cc95f64963962eded6ce94d532dc4846d4468ad3ea7d44c3c20b438c0474d69"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": "3008784",
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "f4251bdbf04ca2471ec8b77bc95ea56380be6262e4ac6d59d6b564ac2e94ab01ac586260c0562ad45f3af666836e271751af87d7f6db6c78f2382c6d4a2858c7"
                            },
                            {
                                "filesize": "28351331",
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "79c654b274003e159f294f6d3690c76b22928b9745c5ca72b1572162be5c47c7225f7973b088c31ae9b5534e8b97d97d68904663be47ee6538893f97d7234ca9"
                            },
                            {
                                "filesize": "22472832",
                                "from": "Firefox-42.0-build2",
                                "hashValue": "33a57ab9e946eff23cd716db81383bca47024c234cbd34bb6533550882d5537f2564bc1dd5401e72ce9863528c2505a07365533ecb3b84c36af59e35df2fef07"
                            },
                            {
                                "filesize": "30597611",
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "82171aa3b131328d54f57a840432fb78093867ce7e6f3f4958277931bd2bf5fbecfdb9ad7a0f4c24375e011d8b7bd6b8a828865189c28928ac0bd6b78ec2e6e9"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "en-ZA": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 52219764,
                                "from": "*",
                                "hashValue": "a4af0b7303733097b480fd12b5faaf6f8e12157854fe8c393ec6bf083273d77480c0e6f09b5a251fd0d0d6340b193dd8f9e6dd914aa33c476af1bff6bf222b31"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 22452152,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "661f8ad7f757a8056f01dc1bdb2c52b19d93353be7a02a455766cf8f879802dd71cf08fb077717eee6e98f6a2e9b3fd35785ed2052dd54d9f2dd67496a543d0b"
                            },
                            {
                                "filesize": 30562035,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "1a5973f7b08bcd31423b86e053ca34b637e2d608e163cef191901b50cb3379400cb6c2ec054e6e8cc1d90ebffc175e682bf7c2e9598014526d31456836923ad1"
                            },
                            {
                                "filesize": 28323176,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "da09d69414547cc6969b627abda6b7df2c34ea77e7ca111ba97a68283f40260f0e85fdebed6842ce99b0adb80aa7f856b692cdb4c0d6e7debe6d7ec4b01cfcf6"
                            },
                            {
                                "filesize": 3008916,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "be3426d953b0bff17ff76e3777c4cea3641ebb35db66a22f20874e87a0ce5f4b8eb3f524d7ff723bc09a1069e79880eb264cc2effd257a7b945cdf22c4d5f64b"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "eo": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 52265574,
                                "from": "*",
                                "hashValue": "c55545a6b134f79187e2d12184c26b50760e7115d98b161dba84d6dd43994d180eab9136410df0051975bd17fbcf8665cd2c7de9161aefb399b983bffab24daf"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 22469991,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "a422f982d21bf8adef6943de033c5a6b5729863be1aebf1fee8941f344f21f38b7fad8e7d7adce80c6188f3d73f91eb8c4ae1e3c6b733d91693cf2d97467b4c3"
                            },
                            {
                                "filesize": 30603637,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "a4a4f97cc710781b545adb3e0a76db1d4f199e2eba1528ed49a9e29576770d0b5b9d9b599f83644ff40b6b50f8b63a41bf366166553468045a43bdeb816dea5b"
                            },
                            {
                                "filesize": 28345759,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "0573b5318ca12b3c427aeb9418bd96b20124f529893d8abcb820eeceb110756db88da9bf7b7973cce1893046c67755f514774c89abf79670e54c0400f61ce831"
                            },
                            {
                                "filesize": 3008913,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "e21937f6a71aea5f99a701ccd1879add51b3d00d0174e473028ef741760ff7bf4fb4a9c82fa5a4e1960acea9241d91c1fa9d7ee9cd8f58764c53737a0ff1afc3"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "es-AR": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 52230069,
                                "from": "*",
                                "hashValue": "7194a88852d72d2043ad6412e1b313680d1960d8cf3769de53e05f30d12ef29cc53a5c70170e661374dd014f5b7e771a8895229b1e81e56d53b9d86a570a9dd3"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 30582921,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "7402148b9582c2d8ad68ae7fe7f6f4e4dfa0bef6822265f041e21b33f1a327d516e8a35788db16e56ec272d14a43c090ae51322749938f8b4eccfb10a4fbd390"
                            },
                            {
                                "filesize": 28334692,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "43e488bc8500e1b0f8f8ad7911e624cd8d63a4a2aae06fb2d9e4dbc24f5a1ef82b86f76dd6092d4c3e4239f4a8ec831b9219bef2ec094a3fc6fc91d1da02d3d8"
                            },
                            {
                                "filesize": 22460399,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "ba6586557311f2163a4b29429a3d2de1b0237994fdfc4d7d1576c859372a5638f1998a5eac61911043faab5496a04a0f62b94ff56e91d99c3e7297535212b7a9"
                            },
                            {
                                "filesize": 3008917,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "ac86a37613caad3ace05a055e62bab01deeb9b9eebb2e534a7a4b46930e5fa40a242f50eec1f9de1e0195f4623d7a60c94487f82b13fe543bbd0d8adad354033"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "es-CL": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 52151433,
                                "from": "*",
                                "hashValue": "61f653b011ddce7a841b872ff164d5ae831acd62046f0c1fd284430f0709b236c813f7cc133d1ad2f9de1856b93728beecd5a2f5691b778aaf195d1c6f42b312"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 22427185,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "67f881eb21c6b5f4c4880a5e6274fa48be40cc618f4dbe36d0a0ec1be591722b9db5cd2cce870988d6a233ff9b1be0b271cd59dc4e2969f9332905a6b06634ea"
                            },
                            {
                                "filesize": 30537963,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "5777a45bf062c67ab65d89269413650a1240923b6d39a914e97eb7cedb0d142df7cd4f995a78a737aa9e8df2d7829534024a5e1270fe4e8d623fdb13697c13e8"
                            },
                            {
                                "filesize": 3008923,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "df0b026a6f644b57a2bb4fc32571bab3f0884c1f6e152248bfc4e7e360027406bda3cc63cb7df2bee58040e357ddcc5bd7cbc7fe1b2387e4984225a350a8a1cc"
                            },
                            {
                                "filesize": 28302943,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "034f807aaf168dd90380a9f6e5b491fefc36f115a178567610f9374151f85982aabe850a8be9c5d94056a0059c1f56f5805e509d90b36125ac90b74946be9fd5"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "es-ES": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 52135956,
                                "from": "*",
                                "hashValue": "541fde15d1635f9d59ddaf00338e27c98d6956a9e4dcecfec16abc86698f60036b32e0879ecedf32c570bc56552079e23488bd6c24ce2a45ec8b9ab132246c00"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 30524099,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "3aec793cdf27a7d4b8b179aead1b7d182108da58aea617d015f974ef1efd68028d19e9eca36770198b18e16cd9c66a459a7d7a0fcd4cc8ae2d4f0d810afaaeb3"
                            },
                            {
                                "filesize": 3008930,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "3527b791375e16626d13439787c7da8e6f25b9cb9c200df350a0480ae951b927e2b692947a59d0a63b6af84dfb76efe9556890f9612a287ceea161aed5955a4e"
                            },
                            {
                                "filesize": 22418575,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "5c2dd50b0df00e2b4955edebbea2926894249e7bc6bc2d66029c14c8335f93bfd9ec3bae3e2dafc7ca37ac7fc5f8c262911a68cf117de57234314e497c264753"
                            },
                            {
                                "filesize": 28291994,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "5d2c7c913a4fbb71e092f74c2e23cb923733539c2c80c251ebff66b9eee0981de2bd4263b9bf0f3da76733a4305c7022cece9e888bfb3eda7f10d703b7da80b5"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "es-MX": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 52235407,
                                "from": "*",
                                "hashValue": "2bc54ad70dcb6efda2c65ac2a50f008fbb3637f267d9003d49c32297a604ba04c413a551b84096cc4f5c2ae3c8625858d1ccb33773ff797089fa03b0198fc6aa"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 28341601,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "be2b8ab4f8f86809ef2a151b91c6ca9f1c062cf3ec192144820d39830c808228efa39b078ec5480fb5b30009d6a080f388af5a91f11b3e67dd2d929885d95e0a"
                            },
                            {
                                "filesize": 3008910,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "d5758bff0da94733c8b86349db9c2f7cc5665631ed1d7a9a29c9f72c6bb02ec08b17a01c82d1d5def1a505312588150f238fd179c4a13585516f129798ef161d"
                            },
                            {
                                "filesize": 30630698,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "22ba7e9e42e6f7ed6545019cd6ed7d094581421c337a5e4e015d355ecf1dea20995914040fb1042929fd9fbbb51232d8ddea9a02fc47cde2de6a27cf483ed2d6"
                            },
                            {
                                "filesize": 22464659,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "d463e57343addbf67c8e7764827a4565154c307de96f11bace9d40ddc721fa5786fcf9370482b58b0de42105883c6abddd3f1090dcf4622858c90703fddf277a"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "et": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53060868,
                                "from": "*",
                                "hashValue": "198f286bc9450f4c0a9cb08a5b29568b4fc17466687b0b9a9d32968866f1db3f96b9f9a35e93daf265d8238dc49191ddbafecedf0ea3e0e700ef89854139ff58"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 22456081,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "e0468c8d4b41a3c22ad921890e4d76b465fa793960c394df2d464a3be9be72ff12d08034ec379ab22900dabcacf8a5e62c6486b69b852c00b9867b5c101c44ba"
                            },
                            {
                                "filesize": 3008755,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "7e3dae747dfc8a024ebb8432b9534f2adcb364d8fe6b06c709a2be86d424c42b8b8c3c27f36bee7d5796cc9c0715d2209ccbf276461bfd8ce416ac0741edd27d"
                            },
                            {
                                "filesize": 30574278,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "dd648599019be108464090227a6b39bd2827e85787b62430c733f70622d020cd7198da445856e03342917a65dc0ddb62c3227cace7fff34c6e5ad7d45156472d"
                            },
                            {
                                "filesize": 28329303,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "01bc14a64f130e5772ad4592d566a52e1329382c50d34576d38da007f80970c69983dc8a159155228102cf401c1be0943920f776b2a238ec58501ad1c1ff0213"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "eu": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 52247623,
                                "from": "*",
                                "hashValue": "f0eb3609c0563a3166378356e37ddb9107ea7cdc8278224ce890830ebdc69645b9ab86d1f1d10a69a08c468ec3f52c188341d8f987fc9c45a15432ecdd4c2ebc"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 22464530,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "c28c2cb43a78514a48bcf233d2b92418cc33dcb0b1f7199011041a09988769139d6638057fc988cfb71333346ef89bd29cdc563c9186a13eeb18de0b95673d8e"
                            },
                            {
                                "filesize": 30618622,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "d2dd0e3c05615c0e5f00a4db0f7ce6777aa416b23ce0bd91dd28263eac713c0cb9b2ffd257abc7d8cc2c03fba1183ad0c440fe432d354061adc88810af9f2066"
                            },
                            {
                                "filesize": 28361579,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "f863b1e4a2acac233eb6904dd6ed326e2bfcb206e984d2dce191af9e1794fa5b10ddfce2511a28dd9ce2dfbc4e8397760d9070b79dd895c17d0034d28f11607e"
                            },
                            {
                                "filesize": 3008959,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "e8aaebc067914aa40959942de15b8493d0c57d400b1800c8f250bd515f22f0b29229a19ab7b65e084ab89f313a1db257e332ae03bdf75255bde34f942062b38e"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "fa": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 52303093,
                                "from": "*",
                                "hashValue": "b3ef446ad06dc77ea440b64e13f38042f9b2b139b605767ca5fcc78f8d6e406db1c41b3faea534ac6588b6c4e5e113911676e24f433d2dd0d8230e5be5a51f97"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 28496499,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "72cd5adc7402c3002d2ca5a488af1725b8bfdac03abfdfacf4a833975ec6befe5b095c8a0e07d8ae645d283e50b620912a039a1735868e1c18264b59b999b512"
                            },
                            {
                                "filesize": 22563924,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "fa103c4b8a4943191a23a758fd98ae34052f42acb13adfcfd16eda9825bf8e5ff0aa3d4ae5e58fafd43d904012b5f4c1c44a647d88044f3f93882b6992572124"
                            },
                            {
                                "filesize": 3008933,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "a9a32dfbdca4d75e3b585b288eae77a72801224b92eea3b48a5905d59f1cd8d6041e078842fbe266d260be0c9f94a5e33310cfbe56aacc8c2a754cf34ee2f259"
                            },
                            {
                                "filesize": 30717752,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "990b4733e636c160330322f03dd05fbcafc221c961ca1572fc01b5ff68b0419d7566c6dee4deb64c7441404401a600f7d9c49b8cdd0b23e54ddb8d7f38e9949c"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "ff": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 52235884,
                                "from": "*",
                                "hashValue": "8a05962ae397b5c51629066e01104b8298d0ca7911e713f64f52bcbe0a092c1c49f6f542f2ab1597a343b99c97c02fbf8d97b91cf43c9c701708bf054f7189b5"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 3008915,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "ffb7953df0ec83d758add722c83bf1c41014ced2eb053ff80b9afebf2c15185f1bb9dd7a116a5c660529166902930e830500ec875acd8d4ba175c8115ff15752"
                            },
                            {
                                "filesize": 28321745,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "09eb7fdf81a49bd895615b90c6b614fd2f78a76e28cbe5ba58e4ee1257985da7b740ec9e8686989e275188dc74c80f10b079ae289f83036e55d6561dc3316ea9"
                            },
                            {
                                "filesize": 30565391,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "038761a06a3749332fd3a5bc8a0dd313c59337106873b1b7ed4364122c076216effe3c9a6bc0879413844b12a966fa22fa0a21ad1b2d2a533c14648a8c990b99"
                            },
                            {
                                "filesize": 22448021,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "24e2db289e5fb6d4447d32a0c8931d7c35f352046677b8c8fabb76661d7c49d4a1ac6217ba649c362a2fe704685ca1a1fb01f95ef273efbcdcaab1407e33da7d"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "fi": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 52225189,
                                "from": "*",
                                "hashValue": "0c948e50e2e8c2f61dc199c757c7b8262402e7b4a292e3d01c5dea70519ba29d7943a7f3259759f791922b23c9e7127cede53d0bf82b8ffcb70aa7ad32167a90"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 22456063,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "f854e00a8170ec6a3afb0bb2bcd6f10c28bdd04e6d7a4b712557b44bf97051654a1574e8e144f365dbd4def816a5d884705296965e1cf719abeda27fd8d38931"
                            },
                            {
                                "filesize": 30566517,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "f550bbb93d9dda94b96082be7294cb0a5e5c15388f17a470023842c1d04681ff6b842483a99d339941ca96cc3fe79fdd24f69fe1deb9d4c29fa9c544cd09ee4d"
                            },
                            {
                                "filesize": 3008917,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "e16c702c3e588fda4683eb36724c0687132f3d80fa264663d5279925cb1a6d34c5ebe53f10978e2c122cc0b504fbd18579d545a247c8f067843ef84ad1992f3a"
                            },
                            {
                                "filesize": 28326087,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "789e27679ba1a3599a2ca07b61241f2ef0f1eda3f8f290b2807d67c18418b5af817325f4451b51c2cfc2afd1eae1bb672ca70ce4e86495281d1484fb4ca63f9c"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "fr": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 52607061,
                                "from": "*",
                                "hashValue": "f23494c9eb3e01ce25043e13242edcc3c006e5aec616749477d509e99bc014415709e2006e8e3ccf14546513e1e8e6c399fc9c2a642942a61bb3cfd2854ffcd5"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 22489722,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "5e03aa3d001dbef13ed6427fe69ff6d1498d7ea2799b187bcce3042c7b9fb88483ec715da94cca5b9a01054d4fbdc2b05a59c089bedded035f49ebd604ab1c14"
                            },
                            {
                                "filesize": 30606622,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "e11a8f00ce7fcd79ac80931a77396b30dd66307918f6af03a5d98e315f74722139de94817ff1839d53d842f6b3c0e33fd4cde9b3eefc44a263cd4ce96b642d9d"
                            },
                            {
                                "filesize": 28361248,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "9c941835f6063308d2b20597abe4c812d9e19e282d321b1bde899b2e37df91f4df7e904b15b090e8cc24f24a5769a7f90e596cbdcc7bb446920d24c4a764fe2f"
                            },
                            {
                                "filesize": 3008854,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "11526b38a10db562b2ed4caa578a31878f0c09d4b8754019c27909b279f9b573183d0e379e8246ca990e857205e189376d7ac1c646d5d08513b79c676f55dde5"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "fy-NL": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 52233913,
                                "from": "*",
                                "hashValue": "d664c86d14f9ea9c65b9f5eb368a09f7600d6092ba4777be63984db936ee0f9114d978886fb618f407500afd0faa25660c26737595096f983898c2753ff4b469"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 3008855,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "41145c57f7e61f20007aa2c81d23297619aa2d31b539b3d656e87109471545cdd6396d05a137727cf9a8046f04c300b7f2c40f7ef22922fb27a9f7eafe268fc5"
                            },
                            {
                                "filesize": 22473923,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "fb5a17b6631ba1e69c149e9e30affc8f50016642fe596b106fe74051b090b0ee35f0755e8eaa5f0d558102195bf0aef9690b2767087a5771595ee282b04f3178"
                            },
                            {
                                "filesize": 30587271,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "593e8769936ab4b19752e2644940cd8600db0e1e2df72cdf18579d576db59bf76545f6004c1ec9ce06e778959aba6444b9182ea30ed53095f6f735356bf02e4c"
                            },
                            {
                                "filesize": 28337430,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "795906582048cc90eba5380a041525436ac55adacf346860f174e4e6a3ed2af69dc98ed619321aa6ee621d880870c49cfeb09ef24da878fae76a53b277bf690a"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "ga-IE": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 52246786,
                                "from": "*",
                                "hashValue": "441c5238862b5f31a13bec62d798fc1367b7390447e4222979eb95ec47a98057229dfed7255968ce9c83e5cb304aff08d386f5645cdc74e1a3b18e48297531bc"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 30596008,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "5e3d3a1326dd4c904d7030a4ada30b87e0b88904819c6ebe3dbf730cb29a95497a80637cd1f9e5eb1313f1ca1ff98eeba0f5a84368179a3cb760cf075b16e82d"
                            },
                            {
                                "filesize": 28350757,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "e456f9ebdba1552a11ac61ad4f9b998dd358fbbfb92d84b23c3e08729a00ca61455cb4fc27357734f5217462263a51520349d1bb47e22b6a747831e37baf5ad3"
                            },
                            {
                                "filesize": 22474086,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "ba275570f1988d5bfbee3cb73b8eb86592de840681c7e857175dd5a1663bc6aafb0e86f75396ab5dc2c71a07073be33ae5d25803bd7e961c719bdab3c784c996"
                            },
                            {
                                "filesize": 3008850,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "f78cac022b47efe29b3dd0732d16aee4847312352792be3d65f5ea927751ae7cbf185e532959488fb6191ad23b9bc097cb3a1f50f8b430ad5e354b9c9942de9e"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "gd": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 52235355,
                                "from": "*",
                                "hashValue": "981340fe8196e781c0ce0b9a8a518a0d7211f0a5ee3189f6d2bb36e2e0d97e4bc430d413aeb5ffba6456718a191a2e63d5f8a47563b324117bf3fe2b3c58324b"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 22465047,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "ae74a915f84d9ba04c20b6f25ffa65cc9cfb60dd9308127d65139e7922c2475ebe5190020acec792d10b2c7f966b90ccd0da5a4e6b1f56ac22d1029f4ba1b31e"
                            },
                            {
                                "filesize": 30583428,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "2e8de48563a93d1e3df4de68287f7955e1eb945634dfc5d27d4ce274419e92fc145b719e762a1dbfb59fd7252bb04fe543dc04789c2313b8aa40f65bb5fb1363"
                            },
                            {
                                "filesize": 3008835,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "9dad6b6fa15aa7869672bf855b87395f2ea3869a0b99f913fc1a18055ad1201219aeaad49ac0b45d118072ac89b0d6d929af3e3a9b1db839dcb847f80c6d9e8b"
                            },
                            {
                                "filesize": 28342234,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "b15d8a60b424c46036db62f354ebca925354eabec8b69f92ed0f91c5c39fb0f26274abb37aa0350aca94f317c29b19aa72c39a7d6ce4e60e9bc78b2a32d671ea"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "gl": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 52224808,
                                "from": "*",
                                "hashValue": "2cd0d20db3a8dd20212e71d69ff0ec305bd3ca5553fdb9eb79b3c91ebf1d5dbc90ebb4dbc03891cc0dfdc94a9c4ed546b44ef4aa0c948cfa4a2888fde0427f42"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 22462694,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "37a1a0b25d227189abd20aab2b40fcb0229541647ab40d4530215dae3479c3c207889488fc6763e7add4cd1f7019a3910b90bee143404c0a51d3b9c692e4d2ca"
                            },
                            {
                                "filesize": 3008758,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "e39f33121779501d3f1b97875fefb0d9a0ff4faa7eddd572914e3cd9b5fac06d8be6747c0d1a54977f2c25842257f5af91ff8501a47928fb23806f26b67fa4ae"
                            },
                            {
                                "filesize": 28444293,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "00d15639984943d2a6b2917f36bd278927e823d0e60fb57078ea22613fda1d0afac5489260f75899f99f6c9f00767857cca6f1518af0f89ecdd3773518b3a5ba"
                            },
                            {
                                "filesize": 30658162,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "0c224d46c76e194ce07db84a21d3ad64d4e35fd426fab8a40011843ad6dba640b1fc35181d34576557e7c1141aaf5e22df78c010614d1e8ab626dade2e58b962"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "gu-IN": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 52265141,
                                "from": "*",
                                "hashValue": "ac99cc90d93369f83eb899bbd92414cfb047e797fcee4ce02ff50a3e8c2ab3a12732df4dad08cfbbd959529ca85779bc9973bb4b4099ff58080817c7dc61fe83"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 3008540,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "b7889b852e075c4cf948c5733a2222e12f5c8874b6287d490727e983bfb8b3b13deaa5b01dc59f2a5802ad9be8bcbab9a1e13957bf35738edc048b9cc37680d8"
                            },
                            {
                                "filesize": 28317970,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "038f9826a4ce8b88c98af9707788e3ad89c9e90b4f0317287e4da4c39a64ff5fce8a04cccbd0b9f0d8506de00e096e8a082e5da0a3598ee42e9102f005047446"
                            },
                            {
                                "filesize": 30561625,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "569111e9042c5587f7f3df6d8b935e722786e5d39f925d096f5d08a2ab6944305689f99e72838b4864127531cbbd8c1a6d0c712ad045cf11347bdeac305fac8c"
                            },
                            {
                                "filesize": 22456135,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "23e03952847599102966f6ef296a2ca49c75a2f4020a4a77cab7f652d9c7b07ecee26110aabeb619e241684a9a325aba31c571466dc3cdcd4167f144dfefb5cb"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "he": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 52253957,
                                "from": "*",
                                "hashValue": "b2eb8056ff911830b9597cc542cfa60b8683783e3605f5c2586de80e1a6cba1ffed5ea90d8399913a9415ca4b0b0081790017b4abc1e01ae171f186630683acb"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 28495836,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "b01e4f8c67a03f0fb53979a6040050b99da691d1092898953ae3e4e359073174b4cf96c3ed20447503f2d6113a03978035a9f0cbea3d5e9531b78b21b976768a"
                            },
                            {
                                "filesize": 3008567,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "fed2a28d3b4378778c78b70b0fb79c71a16971750a55702fa3d20a9be9396fa3b4f5781ea5c02b5d572a3a034a78f470ad0a615548c3fad2aa131773e3ff9cf7"
                            },
                            {
                                "filesize": 30719641,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "06b9257ac32ae8b8fd542d97c61bd53b7beb7ca9ac9b793c3e099de14337d54a8e823125300a339859a58e7572d3fcdfe6bf7271d32587dd605c245e2cec4a18"
                            },
                            {
                                "filesize": 22464500,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "a9a251d0a9ecb0f4ddd563bb229e15465a19bfa0d735cade3a73db3babda176db1a1bd666d494665f48c61f13a45570fc17446d7b2c8f9256eb03a1874db64fe"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "hi-IN": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 52290510,
                                "from": "*",
                                "hashValue": "6fe58345ded7e2d448121b8498182f017af1fe7e9958f7283698f35c311b90821806a4a1e7ee52c00d51d46a7d59a08d6dd9f5c65d5c2cc72891168060a051df"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 22459496,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "c018fbf75bf3a19f226bdc187d73565ef7f87179cdce2871484e5fe1cb96768c2ae3ef8bff3d9b730902a2303f16e44929d6d32a8d68d09dab71e389bcf0c3d7"
                            },
                            {
                                "filesize": 28317974,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "73d3ee34bbcdb6d20fe9be4f23d6f975842a5add1c7cffcfd3273f9ee3974f84b0601f3e5081feb4c44abba16dc958c95ad849127e3471b605c53acfab3de7a8"
                            },
                            {
                                "filesize": 30584346,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "71bac85c4f73da4ca6bf1fab80a6b737a94c9397ebb599a70ee11e6f1a527b349b72109f75108c2b84629df6632bdf0c7081982a9e2640e322dac869a4e1cd94"
                            },
                            {
                                "filesize": 3008522,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "83b075edbc621518356faef351097ed8b6fd30f10e9757b932b772de8e340e8edb6b6fab1299ff4cfd2c9d6e76b3db4a3a2379d6fbfce40cf75f2063a34e75a0"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "hr": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 52259305,
                                "from": "*",
                                "hashValue": "352b93194c5ba6a7842447d74020e6f55f531818fc9ba50a3804672bbfd678f6e881e9f0884081318347a948b9cdc3abc4ce5b8ef596254e12642ce67e1c05dd"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 28342574,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "70157997170fc607e7c16f03342675b377f37e0b3a1eae52d38dc7b27fb95189c657c3d4772775a460e8346fc1f4a8e46dd4db8db11f8fec6dd662f0fc1270dd"
                            },
                            {
                                "filesize": 30623794,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "fc2420db6517ad5762e77fb8acda08fe05cbab44a921911767e87dcc70db19a210d7c52448d483e7b5c7f644de9f4a91a11dec8e59a1e8e2b88da839f711c602"
                            },
                            {
                                "filesize": 3008536,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "33660402131cc6eac82b32f8eb629e01b6065cd2d31d3c1cf31e31c97850fb84099b035204e150bdd5112ba5f4065c2aa2a50c5864d73debedcd3bba93d9192c"
                            },
                            {
                                "filesize": 22462348,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "a91d80585ed3172f2952eaae833bb9fdd5f2b776e21844ec11abf491523393f5e5da1b25e9d109e8a5ba30c17271fe7e69f21504f2e1fe1d22236c0da5c6d2ed"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "hsb": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 52252348,
                                "from": "*",
                                "hashValue": "86c16608d604d8c0d1df7cdde89e06d88000ed320ee8b1d7fc61ed58b7df38f9e5beb87a7724b33f9815d9dbf05771d8721907814e28847a08e4b555bdd6c3ed"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 3008398,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "84031cdc8d907a909eeb2a8ab872ff6f43d3d499ffa3f6427694256fc87a45ba552263567e93f2961e541cb0ff1403cc793b12d905b8c4abddc7218a7a2f6e9f"
                            },
                            {
                                "filesize": 22468677,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "dd3fe789d5348e732fd9c6090a3885828ad980092ba3504cc75539ce7c055456170bdc6c1fcb06f93cf821fbe3385655d8119352e3d87e457bb8faee79011055"
                            },
                            {
                                "filesize": 30610261,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "a3dc12c84c63f546f8e98dfd90a28b4ecdd0a98a0b6dec96b0719c736fd0c325b3714df59801a395f425a6420075824ec9fe8e0c9e9d1ec7277dfa81818fdfdd"
                            },
                            {
                                "filesize": 28363546,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "18a7251fa9614aa19254ee0029c7ecac2c2b339076317a7da847d898a5019d59cb64d4eb0b4589642f51e14011a976c5cced1ae3c4313b180f9413b288d5176c"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "hu": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 52861128,
                                "from": "*",
                                "hashValue": "49e76cbf43857a8a1a52636aa178e4c1bff5e496f73c0b2d499cd2b028e70d870e07b79cfb0163c935471182b09487009b9bcbd63bf5ffdc1ed249e00125be0e"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 3008415,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "90f0623bb536a120ed14ccee780435e87d4c6c055606e4666aae67c3097b84a76487fa3598b7d6b5383d372d42f11dc6e7e8eb7aa970429e0025471c4ae13251"
                            },
                            {
                                "filesize": 22461382,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "a798de5502d0be75ab06d69746d8176cb2cee101223e492f546241000c5c054d1f50f622db1a0c9a78f43304d3dc7f7400e8870709abacafdecf677f609e69df"
                            },
                            {
                                "filesize": 28337108,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "34ce0b119866debd1b4a04d3cfe7b3416985b093fdfd94bc8c5e3932493ae0c3bd75edd21afb302015a1dca77521dca2189de4d97d6b665e84ec5bb1fb9beb9d"
                            },
                            {
                                "filesize": 30587823,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "d95110dfc16ebdec23a1e6156f2dd8f36785d5d59bff30294ead60044c5dc36e3bd787fe05fe9ff32fe67377513a1c3b897c493eac3ba1cbfd511bbe21834580"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "hy-AM": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 52318359,
                                "from": "*",
                                "hashValue": "6f5c03d64e42411ea1e7355f88de9239786b1b430ce2abf97a54ffc0907c4918ddf2e67b34d58dc5062a3b2d13f5fd55098edf15f1ef7886923d90e8e2f373ae"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 22445728,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "dd99535498c55affcaab90de2bcfeb1592ac186587bcaee7c896e4e1a54a3733de14dd71c18fd84e3b88c39061f1e8e9c2ce6cb28076a702f83439c45893f02b"
                            },
                            {
                                "filesize": 3008388,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "9311243d5068c7829fa42ef5e96e14cc5476134a1565021794ed854fce1e3a16b35849fd7bd947c8cd36ae09b10c0859d999497d807ec77368300bb4011a0f35"
                            },
                            {
                                "filesize": 28431460,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "e9119566918c107dfd11b97bd58be395557a6afaa3558358a345e8f97b7716c6dc83b7874eb4d640e7ba9d8c063ce1eca16b24739465209491a4585cb86715d4"
                            },
                            {
                                "filesize": 30679185,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "71f20a6357593eb604dffd4a99469f69ff3640d85cca86eb304a5fe9dd793f3cbc317f578fa1409f46ea24fb75d6265a0a0099a7580287ef5b8e5a03d64d1ac7"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "id": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 52306974,
                                "from": "*",
                                "hashValue": "a35bbe4053522bde7e5713d76c461521849f6f6c34bf68832a86a472f3edf92dd82c714c4a33507f52393b4a79ca8b86b3318f5784d4a28f1067f17f8a7ed4d2"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 28342154,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "7f19b566d8b904dbc13bcc74fe8d039153eb8afc79f5b17cc819138693213bd94910c063159e040ddcc41612b16d48526f2f256db7996b6ddb28bb5d7c27d302"
                            },
                            {
                                "filesize": 3008382,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "b2e05522b95d26b3743b06f5a9b86a142eac780295991319b4abe3d800427c38e585e982c97d12d705b00556d444cf4547c1e26b36c96805a8aa616d25a78280"
                            },
                            {
                                "filesize": 30589978,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "aeb62a4111efa2e9583deecbd94431fb3323daf20c343bfce202c096eac001fcde91008211583c6f08b931c8470f9b2590b61880078ebe1df45a872b6b5c3463"
                            },
                            {
                                "filesize": 22446761,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "04e122f5f8130b7a7a7d2b02b5e31d64635ead312143314190aa8f39fb2559d7e577df459bd22bfdb749c981354af2d86c65957f2a0619ab6504ce70ac3e79f5"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "is": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 52266075,
                                "from": "*",
                                "hashValue": "709c898df34451f82aca01641a63e07bb1dbc24d02734462bde0aeb0209aa934c62d4ce5a6ed2f5d6de2d43c54fde47de847848c03e68d47079350e84fbea744"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 30594853,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "63abb07e64aaff73f0d7bfa8c84837e960bd11c2f0e1b7369d721d7d8746ed286415982d26b258fe5bcfa267a69d8d4fc5fd0184a13ab126547822a7484badc6"
                            },
                            {
                                "filesize": 28344252,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "4fcbd05eb4397af2ace4372d783bd2d9ba903d73bfa614ec56bd7a2c09557133b6dd6aa3695813278271512e2f77ba8ba4423c4746d5abf75d9e6efc56f3b503"
                            },
                            {
                                "filesize": 3008755,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "0d9a4407db73b6870ad04280c8e4de638048aac6e01b9f82dab2a3a1db61d6a76e9e2b76a026d75d13c1d7e923d21ab83a90100fd6a14fa0d1a1cc279547c628"
                            },
                            {
                                "filesize": 22460092,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "767864eacc749e76e04053c3f411f15fd5aa4e67c1e2d660813ee9a9abddd3fd92b8eb1d443d4070445421a788fec1ceb87fbfea59a1fe1c985d2c5801653b9f"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "it": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 52132561,
                                "from": "*",
                                "hashValue": "f04cffa893a437aad8f159aa81e2e846ae0c1db3d11cd9fc479d755b05e963e12e3b4e230b4a270d03732217458283ba36c73922b4d848992fa3c4f35f780c36"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 30522943,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "e2646857a51c3e484d5215f14f6e782eeddfa01174290041a9df6af2536eaf6af628a691d1c29935a7994b4c4a78c2a8641b1285642bb9b7bc27f01f79a086b6"
                            },
                            {
                                "filesize": 28293971,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "036ba8df30092386b569946fd177619547431dd8212f74c7c46845aa6a5f88a7e0ae751148b735e5e1da480a3463c815e2560f16b97c566f91b895c521f6b095"
                            },
                            {
                                "filesize": 3008685,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "2f8a7e316923abfe607d17667be46b80aefe0240948895c14706f419873fda5496b9bcfda7d28594ae1d93a12b5bd58871625ab0aa7806346e8a9bb423ef506b"
                            },
                            {
                                "filesize": 22420844,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "31eb2f8bc1d6f0acbb38c33af31f901e474a98724d677f3e699825e1885908836b6bb3c6ba4600ae9b89245d94342bc0cd23d028775bc9b0fd95f7284134895d"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "ja": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 52496322,
                                "from": "*",
                                "hashValue": "17bcc2046c0064ac7348303a487c01d05f0fc51e43f5a4d7e6ebf370e17c8665ea9c2ccab72ff4f405c67437ce2fb83b3118e6f823539c64ff59401c78c18c07"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 28356136,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "3cf5a461a5864a0743b1d1e65ea92ebaaec0597c2dd7a68e153efb751e53a0e36adfb2bde6e5c17be685e899112195f22efda5419909f8bee627cf18cd64bc76"
                            },
                            {
                                "filesize": 3008549,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "cdae31a6346c78726bf190bd43bf5f2c6143da7f5d41b9098cda1e6e77fa1b9f887378cc2fbef27c508552a9fc4f91a0127eeabd8b1a67e2602565aee55fdab8"
                            },
                            {
                                "filesize": 30599676,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "f94ee9048c6ba2d1be597132fc33bd1c59c0eb5738a6498a34d285917eb1316e6e128dc157ea372d59fb942ca137da49a197cb35b46c8b0e8cca052691791377"
                            },
                            {
                                "filesize": 22469442,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "7e852dbac6d767f7e330c3df5b6a3aa1e373f149b1f2ba4fbac09b69e558adb3e1a2c095365086b1e9d2a1a4261c0874352738d162b6ba429046203cbff83e4b"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "kk": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 52288906,
                                "from": "*",
                                "hashValue": "d241feb3a916df08c217194c5c75b272fcec8d9c9dd33ef946af9aaeb5b209bbd65bbb4734c1b5cd8f56bae9c3bda8f88fdf11f15d57de6b9dbe5decc396d533"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 28431931,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "2e1f141c3d7bc147556ee5f5f12949256257220219f447685ba4d20dcc68288f945b4211b4008e0279369daf50233d770a9b130387753d9caea6ff7a4f52b627"
                            },
                            {
                                "filesize": 30662920,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "fbabb666fcfe28ac88dcadbd3ba8c093849789d23c787d25bd67ea0596d18f2873cb97b604908cb96a3d4c36dbe6d3911b3017cab6283583f9d9ff7a9f311086"
                            },
                            {
                                "filesize": 3008513,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "830a93f9f85c0ea67d42c2c9a08eb2f8c62a2d88ae09460d4ad9b848c404b1c07e4dbc35a40a796b8767d72c4906f7de36ec5dffd2d69653474a25e11be30613"
                            },
                            {
                                "filesize": 22541524,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "59b31b21d8d24a0e87b65d5a234030a7362974c1f175a491e77f5dc6c62aaeeb793085e1ef530b0f105d326de13373daf7fb2cb7156877de3678487bc3f24b86"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "km": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 52590309,
                                "from": "*",
                                "hashValue": "39296a269ae74d58d096d13903828fb21a49308fe19e48e0ae46c4c59428a15c1068e0e0ddde46abf369a28d253c5da7e1488d723d0a32b989e9ca79397846d8"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 28426762,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "8c34bbaaa33a14cbc3a1468c7548816d990f6fab1632b01403fe9fb2633bcee8e8f7c8b73c3ad5e1f3492339e34158f77f0f29ccb3ee9f75c7e001aa9700fe99"
                            },
                            {
                                "filesize": 3008528,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "a36641d2e97aa79f95562c7ce63270fe9e1932042986339c5b4a98d20b1c87b45d1fa14cae8cbed9db806987492d10435621f6dcf767d2996a3e69cbd9f08de6"
                            },
                            {
                                "filesize": 22486396,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "5962eec4c39dc1279a241491913bdbab5d88c8f36ee027ab3d6baff7abde0feee9adae98525a02aa6007a775f64496dd5b772a63d29474ffb869218bc463cfd5"
                            },
                            {
                                "filesize": 30723730,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "5e5d93a56413d9f86250aafdda891d00285a647d5a20ce8731ec83d7df73e5d0256e433f86f52ec91d3b8548f3a76023ff4fc303393916c98f86ce3bd2bb8a58"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "kn": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 52321624,
                                "from": "*",
                                "hashValue": "080c5527a04a4b624b9a5bf68bb21fdb8530bdf21d846e9e986f87d3821c14cc7e3efe77e76bac4ea2e0eedeaacd17c3bcee313149f0256ab194148cb613b02e"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 3008458,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "942daca2d33a10a184bf8f3bd30da06fe406a8258093144fefa6272850c02ae2392e2ead284b61f35881ff94eb1740b41af967e62f8c0c38992704ecaec14d22"
                            },
                            {
                                "filesize": 28391123,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "0f1475cf83c788e2b9e9bf0140c737ed20b3c5bf93162b7e3c5e60b6311db61cdd08a1648946027505b3aab80601e228cfad719c861b1dbc6cdf88bd91995811"
                            },
                            {
                                "filesize": 30638136,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "8f827dbeaa819d813011dc73c10ae70b84172807d3e5a567712417f88f4016d789d91ae473a5337019e1db696c75d31f8271d6ed2dadb3da2c0fec506e2c2095"
                            },
                            {
                                "filesize": 22469897,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "9eeace17ff7d2aa3f8c38085a6dd956f35d7bcf1fa479e19386ba097a7ee7ba05f583f87ac3a2a3bd95055107bafd4da481e09e1b4bb09aea3154a84a326e40e"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "ko": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 52249727,
                                "from": "*",
                                "hashValue": "b45b003b0f582ebd84487f6b2cb916b534baa4528aa9e5de7ca1728fd40c44d8727e73112a4670660e2d8e7474458db740a6f33b6663c61f4ca99f249396f5fb"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 30728887,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "d46b8d81d4a90e035e0ef18f9fc3a5555cf4436780c87387cd888b6df1bb94b98da516538c2873e05a3bdeddd973f3372bc5b1e554c6438bd5f1fc91ad79d520"
                            },
                            {
                                "filesize": 22463874,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "37ddf56b5fb812de759953c14edd7e7e602feb6128f6128b7e56ec86034781f903a32678c41f6f62ce97fef79256a2030abddc919f2279b63d13a65f8cc7da85"
                            },
                            {
                                "filesize": 28505582,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "fa9da4240bd4fdaad86cd4da58a69c0ebeb1986c31613c2703c501a399dd2801fe2c5e6ad733233bdb7384b3c7ef5275d4cf324136f0767ab6eecc7e051524aa"
                            },
                            {
                                "filesize": 3008452,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "fda01e1f902e97db912a13f33964a1d4e0bf42084b84d1b68c7d03c922785b97be4420d769c2722cbf195f006154abcb9252b680a2a5e5e56c3c2e624873eeed"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "lij": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 52403191,
                                "from": "*",
                                "hashValue": "07c2b1e52def804da29391db84484ee45d52a3c9de54d3990ca09b6034126d8e30872683112fa29330943d1d8d88a30f31045e64c6cd1cce4d7f638144c4e36b"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 22670237,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "f3fd8b6abca3781d394768250d724c9a19c638a94a0323b2fc6ffe6b6bef78985863c78fd9f471edcf7ba3adf2ef5cd08563f2a8cf9909b82d8030bb9013360e"
                            },
                            {
                                "filesize": 30715848,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "d68f4508c5a6aa56d43e293a5d45c3c57318c5d60cc5d1ab0e3d8963bd8305c7f4249d239f021b488ea607a8012d3229b3b23f082aa5f20e60b1964831fd1eb4"
                            },
                            {
                                "filesize": 3008452,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "c0d1445d40616786a566cc0b54ebd84f711a9b753118133c7851245a49d064e83c7176313fa1b3cdac7995ae017e77322de2a1b87287fd9bc422381d6883f947"
                            },
                            {
                                "filesize": 28503931,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "f9c6459b503ae007ca743da7c9336603f70a55a14f2ae68bd048070041202fe51a8ae2f596104669005a38a79a70253acdcce4e959eb3b716cb22a99a6588663"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "lt": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 52589541,
                                "from": "*",
                                "hashValue": "14a90d002e0261e1ac283cdf3a96625454221a2eb4f6167917f3e9a157032482b747fe96ca6571501b3a5fa55ba554f8140ee6ba188edb91200d3248f9ae3f86"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 22504644,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "e3ce6ebcc83a6b92ca026d3f185e57c992d7d9fddf7b1ec7d1f48bfa081a2b4c87bc14a07fe02cca08f73101f04eb9b2fbd9b7969bd62e43da639ba7fb81b45c"
                            },
                            {
                                "filesize": 30643760,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "1eff67b7f24de7fd5491423216db36f673e195a85b1f834c9c8e8ceb2f38635e8979812cb98fe62370e376f99a474cd36c0ea173d93e97182ed26a8210fe91f7"
                            },
                            {
                                "filesize": 3008445,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "966afca9c5a76fd014f774f8e7f63a2e3e1fe8e9fe807f7af160191c6da883cf4a4c882133fdd9a1f96b6ecfaa6822ba2da6858aee284b8bbe765d5e77fcf4f7"
                            },
                            {
                                "filesize": 28424762,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "a295c99693b4f3cab26d9ff10de569988679cc0ec4b76eded3e58eb04cb439e47778d9a10e5ec3b9ccc23df1d438388d1af41c5800bd22163c6e55fea06f3051"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "lv": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 52534538,
                                "from": "*",
                                "hashValue": "1a105779c96e758a548dca3a36652eda3d1ea2c45a13d716f5c398ad9c381b1b572ec72d888ea04db59796e650666a7bade4433ee11b4c148fa3a3df5a8b1841"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 30591521,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "47668347312c16caa7910a7f8e99c22319b0df65f98543bed01d5529a98aec74b9a06f69dc608dcf3c9e8dff83ef0b47f1a30d49bc7b50058253ad8b8588d200"
                            },
                            {
                                "filesize": 3008774,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "0119b46df288a1c3b44a2a2d55f107a9f865103b2377f6a41e7ad63a5d70d9b5afa235518407e81ed7032975a552cf916dadda44d706fa6c278938f3b7e070c7"
                            },
                            {
                                "filesize": 22463004,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "42615d1cf6973304ec63acba7f01cd35e1b9a1e6702561f48856555e4734343b50f2c20beeaa7f595dd8dfb1a43332605c82957e285e102a2bf8648b02e85cbb"
                            },
                            {
                                "filesize": 28343867,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "9b283a8cd6eb4d957b4e2acf946e5556e589bfabe286371f186c69154e511f1462fb2cccfaa914511e196c93c888c2228e5a48f881ddea7a29d0387afd4fc98d"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "mai": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 52299833,
                                "from": "*",
                                "hashValue": "74f1a71e3ada45c3a1951fb02ab08a2ba9158e103aa10acd0c52a5d7299f8fbee1dd5b858827b99904fa476bc079c5d84e6b2c1b69c18dd94c5c814ad5cf5b59"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 30585409,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "098d917c3a7994cecaa7a75f3eeb6ae68fafb484c224878c0233237c219a55fbd39cbd85063e6f3d95f52e705c75fdbac1f7dc00aba6bb3515db903a6d6a7884"
                            },
                            {
                                "filesize": 22462483,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "a8a042ecf16a7c8370f704d6410d61eb50df5a02457ebaa2ec8e2eddd1c49bdf66c17b87c49847d408ba7cd67a124ba75a9f930c46a9e1eeb3a8e89e3bc982e8"
                            },
                            {
                                "filesize": 3008698,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "f4f25b18b1d73205f85cbad8b7b788b00a54dd79d69b8e50f35b18570bc044dab3a5f92e0140678b142b5c32f9c5acddd21d692b2ba17b72f1f2203b1755e499"
                            },
                            {
                                "filesize": 28331186,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "0335f1f3eba482c0d70057e5268dc893dd027813432158b3b00c66e07a6d90df22f24bb39b0b98c24727e044332d54da05dcd6949d7897537503d20be7436e5e"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "mk": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53035113,
                                "from": "*",
                                "hashValue": "cb7f79a614422d96d22568b80983b0a5b07fd8d1b9edf51cacced64e2f7f33e9771286ce4e7d211d4d19b537b8aab9e9ffd5cd99016411264adea2d46b89f260"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 3008748,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "8d054d67236843335ce19f7c653ab870e84ac584314d042812e0edad2733dbf5d972764576fbc7bc7ecec9cd1cdc1f947f42ae2b232821dcd251d137d124b9bc"
                            },
                            {
                                "filesize": 30603390,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "ed1bc8a7695b05ea5a5dbd333af50c508e11f2cf328d7c756e5afa42aeb7b4f82ecf15e3c056b8a89728f01698cddd79f8dccab9b091113bb5f06fb6180446d7"
                            },
                            {
                                "filesize": 28346244,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "521ac1b693776a9a2fef9b376c1b742460ec75cc0dd78c7c68c67b20135f13210d36f303246ad560c31bc191f0d5b7081da10d9dbb292d9d269f0df848653cec"
                            },
                            {
                                "filesize": 22463827,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "5620d5223e57b8980a554279cd39858deecc5b3f4fe57da69d7c4347d682a01a8807bab5b39974ed700ad65200318b6366c682ea28020012bcbd1e533efee54b"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "ml": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 52311661,
                                "from": "*",
                                "hashValue": "6b80fd6bdd407d95dd0acd965698c8a760e34488d92b9113424f747533f7e99d35e51c77c18ccebfdc9e56a6db70a9a69beafb2e25c489b84932e50a9adf8bd6"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 22463563,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "124d3509d85137eb4a02da3293ec5d2b2cc43d18532f6c8def34f9f56aa027f7c02f01e64634e4b4764681b2f82252e5380f91360819887ace8d5b4d39c9d269"
                            },
                            {
                                "filesize": 30716345,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "1639ca0db7a8de972d149a26ee2d753d198660366a925a02e232c9baf6396853a7915aeaa982cbf272658538bf86125c0c3e733a532471c29db4fdbb58d4ec60"
                            },
                            {
                                "filesize": 3008725,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "1e2c24b99d1f8934e3c370affb72b207f731ef8a0022174bc6873f8ce2c82f8781ed83886133a2cfc9028ae4b0ed4cdac066351c71d5f4f45b56fcad0c482f74"
                            },
                            {
                                "filesize": 28504104,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "60e65991f1cc7f2b210032160b5f1b575ded1fe3abbb865ccd9803ae8eedff860c96286eb57a1bdc7b5a52cb316196a67b170ec5cb627df2b241bdb75f336060"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "mr": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 52299225,
                                "from": "*",
                                "hashValue": "185297e2fde4a145e82208228875fd52a98e738f3e6197e64547dea3c93dcaba6c3cc94b2dc0ef4ab2dfba4184e44fe7c47315a30b2d59cf3f255da1ff9ab0d8"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 3008498,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "bd105db39792b78895d5d540b837abd5c1509860eec37a82a7dcb65fa17815fe9eed3dcc8c72255c960766edffc59ece2a78f75eff72be9d92c9e1f8959a32cd"
                            },
                            {
                                "filesize": 28495419,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "544dea0cd76f9bc8a064c169270706fa767c3af582b7889f0845c0b7086dfaa63640a11a6be3d759887bb09bb9012f4d83e08a64e3b2c61a889038bfe4d32520"
                            },
                            {
                                "filesize": 30706375,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "7f00520901534fe8705b5354ff4203f1e2993c4cca309aeb9a0d5bbc388195cba593ead8a97ba727839f4d520b1b56500f060d2270841dfe26a9cc5c6685d39d"
                            },
                            {
                                "filesize": 22469669,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "adbec223199a12eea448d2a5baea32cdfe2854a4ed669e9f843077aaf8f4ab38dd5a23730596770d270a3e9b70a062cb6295586e8e1aca5dc28d2c11240b03fe"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "ms": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 52276183,
                                "from": "*",
                                "hashValue": "905416f4c6b13911340a095d11fc20db487438709528fdd39a192c23231d0bd9aecc3ad4dd8dea3b44c1afe59f2bf3df97c5550ed835dfeae41f5e5dcf4f4171"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 22439366,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "4cc68a699c1e1867a62d969d70b02e7d234ed2c0eacec1a0a2ae7a01f61af49234e062de3e6b86ad763065b20f3753932072990e3a02398099b4308e3f1d5dae"
                            },
                            {
                                "filesize": 30659411,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "7c91e827af787d3aab5be88450e3bef752416c493f538f59ff187e327e886b4cfc9694a771e4df3abfceb0864978171d8ef0c9e8b06d7b8bb84b7b64a0debd94"
                            },
                            {
                                "filesize": 3008520,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "598b9d78d8af986527db6f57054512b2704203129bc80f946053908829b817228bf02168189cd25e39da7b18b8a4c5e1604b26797e7bc67cbe37cadcebb64728"
                            },
                            {
                                "filesize": 28438120,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "c1c1476b24edb479ef71927a095b16a92c3df9f1aba3658524f412f1c936f24401e8ea12aa5938cd273fbf80a9338b6402c600d1af49e34cdf70209a57c37f14"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "nb-NO": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 52225149,
                                "from": "*",
                                "hashValue": "3096d81e695f716a402b8b398a260c83d07aea53fe12ef36262f8ce0bd67be434de3fcb559a1d2a8b9dbead468bf417da35df9ddff020caf7354329944c4b097"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 3008491,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "efaa83a0f14e839b51a431cc0133f48ac82307c8260aba5fef0b1fb9d43568780a431499427574a25aee3aa7b8b2d6f3b5b5ba9e76c754f3719803eeabe59e65"
                            },
                            {
                                "filesize": 30571702,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "43a41bc31e55c6d0228f21bb8966c5d32f72ae9e51d1edb69dc26aca219722028a293d24649e0795e36612deac0ebf79b52937ca92b5c7bdb20231e48f68ca3c"
                            },
                            {
                                "filesize": 22453833,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "7295993dfa0da28fb7c9972b359e82e1ab07fea9f3d7cba6ce202a48cfce740d57934ccfb3d52f71904d1a1f6908ec553b58ab78b4e6da0f8b892c1fbf6d7c5c"
                            },
                            {
                                "filesize": 28325052,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "6572c0416f37710d2eeb07204d15177af294ac039ae783cdf69e6ef0f0537d82bc10ff49792a7128bbb427c63139056d3042a0d46c2511bb3c7c09d6b6708135"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "nl": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 52988744,
                                "from": "*",
                                "hashValue": "38f9f8d64ac3ffb10f96e8c62d52ccdf93082d77d53479127c6ee11d0a2b292536d2e6bedbfd9da90a2fef6fef080f3f74afcb84e789b820a73efca0f3cf20c3"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 28338018,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "0d51730623f2cef69c10d2bf1c255d0e83852d156e55179685c02077e17c10fe9dfd1a7f9a748d6d49aad27bb6cc2f409e3668567f7617276b60a137295555cd"
                            },
                            {
                                "filesize": 30584080,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "8eb5d59d8d91af5f4fda37ee67c182929e2abf9aa273340f22af296d6888cac4b6894fd3770f5c45d248b8df7b9f13d2d3268d92d05fc07634a27bc387dc242a"
                            },
                            {
                                "filesize": 3008543,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "58b72160f688afa92ad6c66b4ba7468a06ac850cc3e16f163d1901ea670bbffe18a765bf45dedd13cbf98b13bcd56e516ce98a31022e8a845a4b1da10f086e18"
                            },
                            {
                                "filesize": 22468329,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "5255de0b3a00d759c8717ee400b02144d00772d8839026acdfb5c0ad81a4c80e89e60b11afac0b6e840e9d630e56e3549350f5adc15a2279ebd69921d7461485"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "nn-NO": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 52220717,
                                "from": "*",
                                "hashValue": "430297a6fb83f6893732d984676798060a4dbf2a87966ba1ebdcae24ea4ac8c29c626251d3dfb7290de95494ca1992562f9ff3a33c8f0f20183fd23a931c2686"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 28370314,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "8e5274311e45ff7b5ae38d4afa95cc1eb43b4e1709295556bf72914286dcd8145df5fcd63780ac662501c5982ea59f0babd24e76fdb8f812af1c6a5ab8e381ae"
                            },
                            {
                                "filesize": 3008438,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "0467a5868dc004a8b756d619a8a5749a50e3954702c6c58f409d0feff8a581a4eb05a18b5d293be075f5ad3c2d2ec738a2edd3c6b5ded4fdab29684ff5764f69"
                            },
                            {
                                "filesize": 30583084,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "ad722c471ffaa080b2b35552b612deb937f03b91a36fc52dc41858de50696c0497b49b361727fea4df15cfd546eb84a2a8b13e8bba068aada205bc366721744d"
                            },
                            {
                                "filesize": 22451798,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "467ee40473ac8e9721e32c83b8ffb2934b908bd947d7bbe2cb21aabad587045317afc7ae0c030f1c918945e5efe1a6400dc9066b17728b4d2af931c7d9f32ae9"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "or": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 52538670,
                                "from": "*",
                                "hashValue": "89527fb581a809d8d364ca3cf7585bd4fc7f65cea3ee10b37af6b54b9dcdd5204400eb37a3eedf99ed116032e8c24655cd5fc716f13b64b1e48054ed8169e852"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 3008741,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "6c57d95fa5b3faf135edc220f6e6648cb2aaea62fea00da7d588d459377381f4fee82843038b8916973375b830d99e681faa29429f085dbd51f7bf5cacf2e638"
                            },
                            {
                                "filesize": 28345334,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "0250030a6c594d8387b7ebb5dd972ae0ae8b5c15340133c8b2d7e6b22e8bbe02d68b35010cc28953910e038f45613630b0420f73fdca1e70283166680669fa2a"
                            },
                            {
                                "filesize": 30596331,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "10d0b9f4495bd6000cc275fd711a8e8708857b4941418b6ac1ea2c7c7d578c2bd7fe6c08d7d5ba61db7b69612d853fe2c852da101d927c18ac5c1ca14ee5311c"
                            },
                            {
                                "filesize": 22468345,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "04cf4fccb759dde88ee2ebc277eeda4e60838803dfd910aad56040d560e5943d17a292675cc967a5e68413211efbab97b5e3a2877c0c65e0b5ce2ee70506cb93"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "pa-IN": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 52281135,
                                "from": "*",
                                "hashValue": "4e592b59c3f53320940865d3185ae1e65b918dd1ccddec1014659c6edd281629fba572dc9a716fd41516cea852e29a08cd680a70eb5697e8e5ee32a573188bef"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 3008656,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "45522802fd360a1bcfe1a1e35ce13758ade23cecf2b3e8afa6cacbdb314aab93127bc93e50d9a09677f4054bbca687ad1883a55b71c2847d8c5fca86a729d3cb"
                            },
                            {
                                "filesize": 30580446,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "4c1ef67e9c5e94aee84458ae006114b77b62388bf1ac01e90c5dd7b2d2487bba3ecc7ba8abe0585e17ed0d6907448fc43b489e9d524b150474cc0d9a5da8e99f"
                            },
                            {
                                "filesize": 22463549,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "ac2165557edfbd0933257a3926e8027c5a7320597c64baed4d45dccae449b32f76579ba924590e6878a356a93797f909bea51cdbaf882d278de4e460307b14a1"
                            },
                            {
                                "filesize": 28332345,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "d8143c0aaa615bb4a0487bd26ea469c25b551590562f0b1e0c07ef3eb4f067a7cf0426b76416a3539752520be068076421341e4c39d6efe6770bce73dce3ab43"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "pl": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53299940,
                                "from": "*",
                                "hashValue": "9e79c89ddf0d6ba685e0740c39ef06f5e578e44e8987719a3d4bd95ff152f329ae3ac3ab10010cebc425bde326286494d190900958d72a126cde3c79d68903e7"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 28305658,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "7ed455e4cdc178cc026615e55048b72777b6ef77d138fae926f8a76201bf11445ed108ecf10b8d6bc2b5fd42911fd12dfad61bdfaa2030b627c63b54f120e7e7"
                            },
                            {
                                "filesize": 3008687,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "8b9eca9ac6359d29c75e3289fae1207dcb38616a8730873c5d29de3b3b6a4cd19a3a4e23e3529db3cbe597ea1f06144de79fd4817099e5b076367cececac54de"
                            },
                            {
                                "filesize": 22435823,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "5bc3be23cdddd82f447d5a0f9fb2b55bb4df1059fad32d35b54b7e6db8f59d9ca8e997332b9d97e750d843638d01babe8cf0a935b36a0b64fb13f45a3c8f5131"
                            },
                            {
                                "filesize": 30546374,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "eda5eb0e1ab4305acf40492355b63b0b7d2eb66523894e47c5275760ee12b215bb9acdc90ec0de3ae05ba23034c7aadef5bdff6c3d280301be6bc4ae66f6ac09"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "pt-BR": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 52422517,
                                "from": "*",
                                "hashValue": "fdeb57997ffe1deac927bb92cf2c67e506046289d6b9bca8d86c386b2b33aaff5c94ff00db922a7f409464be5c2c3e223d0560a2a5b771bbd28a9d341a252fca"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 22449844,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "a03e68e7b61f31a74a726c72156b9adeb6689b32ae7f858814aa1b4a98d1156eed882042bd4d399fbd6030ebba5f15fb9458b11f15131083a70d7fc9a4876827"
                            },
                            {
                                "filesize": 3008442,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "c5c655622f1fa54046440a3aafae0f10ed987d78d16e6c0d4840172c10a95ba185fb27409865712f2b6598e695229329069f96dd0586eda09db361138d8d067f"
                            },
                            {
                                "filesize": 30654426,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "c252d775ccf1416a02ecba6b3c45f6be8b6dcf01399bd98734ae3ef812f9e0c61b05b5c5d8053fc025f69ef951bbfd7616280c65130b8dceae062d07fce289fb"
                            },
                            {
                                "filesize": 28350352,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "ec8fd0163d8e777c9565a61440662be377ae7da59c9c4b25e8e40cba86f656ff2c934d85c7a25f94460db26ef94eac174c6f702c982d3156723d1c6fceff9de7"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "pt-PT": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 52413366,
                                "from": "*",
                                "hashValue": "dfec38d61b454d252649fe8dad0176b2233b9b88fe99f89e5eeb781f01defceeb19c79f6dbe18d40779671c97635c46f0c1ac834951ab2ccb84b442a7bab2aa8"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 30698850,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "3f9041aa53e047c420a433acbf8434d3432a82a7a2090d7889e1f330e9d59f83809fdf1930828d3027a1f9622f628f0d374588092b2ed838c212a80246502992"
                            },
                            {
                                "filesize": 3008415,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "7ef45a66c9feb0f0dc3f652c9116c5f037c0c6c3ebcbf5552c0dc95ae6dc1771ea0db7284414889f3d3a410849cbd1712391f114a55e42249a5bb08072f70063"
                            },
                            {
                                "filesize": 22539041,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "2239ec9e28f0b1dad9650468d2178d658c9c9c2614586174463af936159f0925f9a5216dc5cc625175ac233369622a0d2e4f29cf19b95870cdc8df8a05f8d9f2"
                            },
                            {
                                "filesize": 28431998,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "b5e51b3250341ccd1bccbb9982be2f8068586834413fd5c8db852fada605614c6c824b7fc64a90a38ac4e870e28746424a6fc412c0a47799d3b0c1a8eef9e4a2"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "rm": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 52230611,
                                "from": "*",
                                "hashValue": "2fc11b5ef1376114e27e44dea4adec123674327dba9af4cc1419686f7ec0d6feb9ee0bc8bf2884cf4f0b09677a8686e0b1eb9d3618b0783e4cb7c3f5585188ad"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 3008446,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "2482b3a774d701553637750ee2ac751a44af57f3bb2cc6853a55e7b13cac62fce509948757f5265cd6d3c6a40231062c19349bb11e3684fc0c46f10577730e52"
                            },
                            {
                                "filesize": 28433725,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "9fd718c83f26206832c72c5bf625c616946d3a467c001ff306408f0112d44c02c8eda815e2aa15dbd55becb736f175b02a28083556efbf3ae722213c25b92328"
                            },
                            {
                                "filesize": 22449467,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "f6dac16f4dc6e7448b064d73267f673d9dba7e27ca905af901951aca8ba75a3333f5e423f37acd0deab26438e095962827597d2b885ed9736e97391905f13e52"
                            },
                            {
                                "filesize": 30646457,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "6dd9865e3bc8d5dde2324d4b411f8682b3f625c0b042cc5324e459612e06c8898d12608446a4ff6757ff0dc54d7573daf6463df2f7b0cfb0e6f18d95eaa0b804"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "ro": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 52915737,
                                "from": "*",
                                "hashValue": "cd4b76169d7714a93e78aeece7db685030eda189dd2f9af860dd44edb700078090eb34c236f7dbea7b69bd9636c9ee8fdb481753aed0350b9a88c964e34c7a0b"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 30719085,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "d208895aa749c196d6304f03ccae2e8d694c1a3abbfa54d8f5747367dca565ef7d1480a7662d72dbb57794f64d6f878acb1a14c312c96b76433a506865af1660"
                            },
                            {
                                "filesize": 3008430,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "a15aef562c16494f1c6d97a3766cad1bf0db6e216816bee267df6385dd324145c1455b06d6adf97fddd849769eb448bcc90efa0c30149b8bdd4840c465583356"
                            },
                            {
                                "filesize": 22477204,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "f17a72fc688d67930254478988e6a15a25b57c95d71af5b0bd2bd953b65f77f0b24b39b534fdb3a15069eb3b27c7ed4e59017af1fac0658eacd38d458491f1c6"
                            },
                            {
                                "filesize": 28493618,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "723e2a239ecb6498fc88a1193c2e49d40538d8ad145d111f8c8dd66bd5720905a6531e86f5d2e186488db0423e7583bf11e125d62d8ecb399b45d9bf133db9f3"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "ru": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 52710922,
                                "from": "*",
                                "hashValue": "5213d165ac85992a13853693ac20a458c9adba55b4f66b751d2eb09444467da48c0f42aedfd31a2c16ed0de9b75ee71f14bd9ae506b4262ac9fb86d2eb9cb4e7"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 22436749,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "1c31c84185e272a76a32bf728eb7b79329ad34a4c126f72f57db5b200246cb13f86ebf61e79392aaca3fa6c9a02246836ee5ea3afe48f77bfdcf963e5093c005"
                            },
                            {
                                "filesize": 30544906,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "a7b3500fdb1700a388ca907e6725f9bb9159d018fc7e0b664a629d901985c62f9a61e6273d5473f18b9ef13671536b54056372234967e16497f9b0ade74079e0"
                            },
                            {
                                "filesize": 3008325,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "88b8f2ec0d897807223b22e7bafa5cd2ce8791dd5fe90fce78e37777f3698650c5f355d4b4e0fefc8953d2902be60dd9a3d94820c959415d57ea05d3b6b11b2c"
                            },
                            {
                                "filesize": 28307026,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "0c49e8ab56c2aa2305349bf15025d6021fdd8e7651877ab1e78356d0b6cf73dd2773b099771539720de19395372e8ae16be0f8870810d5da34d626fb31eeaf5f"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "si": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 52321692,
                                "from": "*",
                                "hashValue": "dc8e675e93eee0f6a77d094dc46a010f0fe23e135b35662c1c6e578f464c574a528aabc3be765b5c4c9391d6d1c802810714a8e2c9076b87b4ab473cc3ffc00a"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 22471356,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "f685f046409d6002a7cfd2f934e0c536bcdf15760d32d4a731788a9e2fc40315e24a6d2dbc66761b1c3c9c6d1517939cadd913b95d8496e684d937ff52f7e132"
                            },
                            {
                                "filesize": 30727206,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "67e42d876bb84f08ea1ff70357e228ecad8167777bcb01c4ca7b8f7fd2def20accb932515feac33383e8ca86bb1c218c13d0f570b9c1fc6bfa7e9dfe802b107b"
                            },
                            {
                                "filesize": 3008307,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "bb95d45a7aeb6329efa1a944f0139959673172e7cfc7379d1bc472bd398b0f3365f2dbad80f89cb9ed8f44fa351aa2bb510f9a65f56b3f5431fc972e573cb047"
                            },
                            {
                                "filesize": 28503801,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "709f56874d6b3ea3493f5429a5b641bb9abd3bae56695e0ed60f440039df5e210016d8b1feb93ac73ee6e603410e0bb4230dc90d4dd6f8036676d2a21596a6c0"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "sk": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53149776,
                                "from": "*",
                                "hashValue": "e8b61037d369a5366d60c7ce8733f46aac715439599c29849da4a2e53f36a12a4a0915007aea66db2f83944dcf510e4b512716a76549bc76b9a1edbc9a7e0a7a"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 30583045,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "0af73821f11481a750b6100211ee4e1826445b9964e1b689200be085df93caab8301d252ca8ee2dd80097c43671b4082aba31ebd1928d5f8ea9830b5607f6091"
                            },
                            {
                                "filesize": 3008764,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "95ea6a06e3403b889c68a34ff4e82eca0bad95af15dc490207c4190f9f6079638d936a4c826643bf0b183eab3cabb0e65b8993683f27f7e9dfd485fe17183d74"
                            },
                            {
                                "filesize": 22467451,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "84fd2d25de4d10f90d4c59b63337fceafd17edfc29bd17b3c4c3fc662dfd01fa08053a68505d1adfe3ba16560dfe15fd8b72d0f55d4b5fe6d8bbf7419ef8b15d"
                            },
                            {
                                "filesize": 28331120,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "1234fc08d27ae38e3aae46a2419918f1047fe48c3ac3321bdb3d0973a63b3ba5ba1cf767543b98efec30f05ce8f63ec6393e4375470bcddf30a24a561e5b0aaa"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "sl": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 52223539,
                                "from": "*",
                                "hashValue": "51229e59403185a96be957392ffd2b0abfd36a78005d0f2ac17a4ee888722996e0a356054a12287872d7ae3240d7dd6e344de66a42ca5cfe0f72c5a00a656236"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 30582374,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "c363abc41edf18e95fed8d1fe0e1ea897d6daa0c6a7e2bf7325fa520d16e0f52deb761c949b3ca454f8e7acdb861683636aeee36b8eb3b53f1a73b4acae927f9"
                            },
                            {
                                "filesize": 3008610,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "5fb749dc93c294656a60c4f33b8e4c3205cd8f98b3b9acdb0eb56221a8706381f584f1aec1fd5be5dfa72bd9c3e6de96f38fd5c132e39921843d93fcb835f8f7"
                            },
                            {
                                "filesize": 22458538,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "6d0407abf57d7ac225064183378e70bb0ce5cbec58d799ebdcc3493b27757ef24e5d1a002d12210805d74972ee9966c1d4e8db4c6b2a10e6cfacfc5ee808624d"
                            },
                            {
                                "filesize": 28337391,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "2495268f59d10dedde447dfcddec93bc282198d860146eb851c548d8ca10d30c71fdf7909245ba1952ff70a4cb2e3c00355cbd62a34d059f86f51d5cccba4e67"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "son": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 52229253,
                                "from": "*",
                                "hashValue": "786b54624081ec02db7aeabb3eed8484e242f3ec692b8781800eb94ddc7acaa76a5440bac7b320a01a238ea475eaae4eb073e2d8a6a2acc4822463b4072c2ecb"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 28377442,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "900cb47d7a7928983ac7100c4faf582f0a78157934138d042ff104d44fcb5b3c280f037abe7fec63b655abd0215f5dcd9ab468fc9ccfe2a68f1959fa8542e23d"
                            },
                            {
                                "filesize": 30617367,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "45156ef21087f4e9f159b71032cde2f314b0b21968d66dacb0577037253dda956c8b7374f5a8c05a94eb0fe477a9313923008bd5fb0dfc23020cc8b3568dd807"
                            },
                            {
                                "filesize": 3008574,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "192abd9090dcf7d485b5d98f69684dd40b14458e1bbe2b2fbf93977daa652391c7c823dd452405bece2629d008f6a097fe6c68f2edc6d4c8694312c595c51a68"
                            },
                            {
                                "filesize": 22452983,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "a4c50b58779dc3888237f8461d1c129c943818d3437ffad79d0336d0c9966a0db2358ee266fb15ff21a40f3c3775b700369046edd1fb33853167c984146d70f3"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "sq": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 52267893,
                                "from": "*",
                                "hashValue": "f213435cfc7067666a330ad845a108c9b326441e43d488b0b0abd3d115a852414d8cc31400e1b2b92a29b74d808a8c52876d491b5ea7d35f27b27744893816db"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 3008515,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "7931787118cb4b9370979f9b93b2944bd7f99fb0ffbbeea332f3bd4e33b94f7dd0569894c81fe3e3bf925e17e986615ce5b662173ca2faa1b704a884dbafa821"
                            },
                            {
                                "filesize": 30619977,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "a5ffd4ae15a698ba4ef14ffce3a28821678673a0b3859b9a3b23599a08229cf0a1769382396728a64108ce7f1957190c29c04af73f43742ee9d06a3bac9e151b"
                            },
                            {
                                "filesize": 28396954,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "07def7043e3fb589ac82f437ea9269118488ead43e7ba360d321b1d2443571a7f01e4deb44603a7acf46d7fbcc999687e75785bf6c20a1e8543317f8e590f161"
                            },
                            {
                                "filesize": 22469294,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "f03d3b387320aeaca0b0517808ead5431be0cedeb69cc8f96e4770fe7e2df8a7d14f08b68715f4d84193496626f10582c73f6053efa0fb24475d00221901dab7"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "sr": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 54160604,
                                "from": "*",
                                "hashValue": "f68822e85a2d1e57ec2427db660b2e7ebb648aad381cb58921b91ebf9732f1c344ea61e7f57a059d5993acbeb865cb4247021abc77afee018f09b943b70a81b2"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 28450354,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "100338638def20f0db087b4cfc92b8d4592397347cf749a2a755a7171698476540de2b437c1afe00e424a775c5e6cd910309e672dddd902e486ebc218e4c2ce7"
                            },
                            {
                                "filesize": 3008534,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "db80e363b610b5034a0983c82f58d08642a2a240a4585df2a3cd7c2ed4e78f6692cfde36c82c9d46a1c2830ca5c3daebcee89abfd0513d463c8923ae11f0c22b"
                            },
                            {
                                "filesize": 22462809,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "eb9021870b0c654c0488778a8fc84ce8f6b2004ebcb570781a198627a567c602c6a2171df77e36a519422255c3908bbe854e0339f8dba51cd9c9ad1a629f1065"
                            },
                            {
                                "filesize": 30684907,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "3c40a09e545dcd4b116dda018ba43d68af588fd1ce52d2c355abad5b60e8b805753af7f9dd02896152cc7b832081f7dca0ec114cf475402a0bb7804a8c96665a"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "sv-SE": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 52857527,
                                "from": "*",
                                "hashValue": "34e6bc7019de24365b93f0805bc32de18e08bda37c87ee6ac4ee6ad87d39e05058f27ba044e005fa20ef72dc64c17a1b17680502fb7834bca1be2d9e831eb474"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 22447447,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "db96e8c7889e8690a0c4e6b36dd30fffb55ad7a30f315c4e5498f4ee746cf65b59e11156ba3b742128bc5d4177c54dda3497574ad7dab539d62925d7839c89de"
                            },
                            {
                                "filesize": 30588531,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "a0fef5167fca0a2ff6dc4e8656859dde5d520b714274b1127679fe48d2e66d2c9a3412d7efd7360922b45a7a5df5709d95bfe84236109f1827964c9434933902"
                            },
                            {
                                "filesize": 3008554,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "1a2aca32f076841bd7e63814776418c8d4ae5481ba07ada81b378bea759d08141fb6b4a9f06593883e3ccfb044e2443b592b47ae8ac907dc74d2c6113a64cb94"
                            },
                            {
                                "filesize": 28346031,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "eccb8da552cac2a64b6f1d3e75aa92dd062c41a84079cb6fa0e80f23d8fb85a4009bc9d95e838f2f6a0274af071188ffdf73e1f3542e766e3291619f159b9c6e"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "ta": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 52548164,
                                "from": "*",
                                "hashValue": "582f22782a7bb5ae1d88fe0f3ffe80f07b2c8e563217747e5c8dbbaeb95535d3ca03c20958fcfdae9597d3c0329a22239bd3c294bc6e649f6b0fed4b64a1b504"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 28333730,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "e1d0e42df846426d1b4353362ddb12f4c0b2624b5acd6f2f4d237a63974f629204c235dbdf708d98391699064ccdf25449afdd2d6c68824458140e400d0a8399"
                            },
                            {
                                "filesize": 3008550,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "f00029f23115ba03c5ca3207cad1e1a128553019eb177e5f6868aea0062cb3b2be5e7fca3968eda907bf43ed2d961359785799c5328b421daf9a68ae33a9073a"
                            },
                            {
                                "filesize": 30600223,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "49aadabd48997b39f2fc960867b356c2debbc2c05363b293fd25d087e6b24989ea41e23122a2c651400440d591233340807083bb994d0e1d33017d0da0993b18"
                            },
                            {
                                "filesize": 22459804,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "618eee7e2bd1e2345b09f90f11bb572423600516536fcb504430ca9dbc3d476017b4be3acd659ad0ed5ed4fdb8f6bb6bc5610f5222ae5037f7b8a6879ca5bc25"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "te": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 52311430,
                                "from": "*",
                                "hashValue": "07d1ab9f3cf3fc53cdab74f989ec425ca40bda9eaad98299fe9f546e464addf9310082c0e517676e752ab18cb9d17b84affa1ac552ccfb01e629dc757d22c254"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 22444396,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "4c3e3afffc006deac5dabfbf6e61b5b02184f9cc96d71c6458751275685e1ff94a33e967dc3b101acaf3311a102dc60ce128efd62f5ffe7cbcee6f0e7de1559e"
                            },
                            {
                                "filesize": 3008503,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "a0c28fb11f5817df5805d1a0f3b377b185fe51d81855433b13c518aebe0b14649ac09cf51298be9a8a432d966ef618f03f4ea15db02d603f3e57c80ed341f800"
                            },
                            {
                                "filesize": 28451499,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "d7b63c60dd5ae6b495161aed5e256eb1747890dbc05ee134162901b0878db6a3bc8b736c7da7d61c60e3ad94a9ea3db766135413b30715db4a72430a71e55b15"
                            },
                            {
                                "filesize": 30665342,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "3c385f6d18972b64ab8de4691bbb8af9fa0f97d7795e5aebf252b2cf5952588786dc1549c64495869b1a4b9d469f5eaa736660ad1a843e3f82ad1d34da0aae70"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "th": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 52320025,
                                "from": "*",
                                "hashValue": "026546794223fdac2dac2e6d5a750855da0edecbd66c29cc5160eead32c84fa5886224c51e0054109c9ef4c99594a1ac0fe8c65675fbbf2ad1b330e6bb5a243f"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 28441616,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "962c68e878e67776ec90a6636b30f9a6880bff3f68fbf0ea22c271412a4f44ac50bfdad94e449e686c140380875fb7fd713a19aacf7d8eebea1470b9d933fc72"
                            },
                            {
                                "filesize": 30664578,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "6e17035e29338c79ac5b197843e918c82fd05298a780829774319cae5ceae22ed743ad0860a586b483a2858dda7894f3b3e606493657d5708943aa2ae59f597e"
                            },
                            {
                                "filesize": 3008720,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "cf322c11d2d12b793b6b2025478a464310381f393c731c83fda8ab2b40c2c5b5ae84910c41d1073f2b2af5a881d9d374c100cac97de158d8efa2e728e5238293"
                            },
                            {
                                "filesize": 22461375,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "9dac51673b8bfda237a509df72b4a2f172492eb842d8411ddab93990c19e48fe15c851e60dae9651c1b025267acb460d6edf22c4198051b33f7f9fa6591790e4"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "tr": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 52264411,
                                "from": "*",
                                "hashValue": "ddf8c5eceef1af2e91bf2238df67bfc258009198b9a59da2b1593bf553703d698c9338ee7a0a18b2e4532f433fbbf5314838d1e7e2055bfed0914f39d1aa68c0"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 30631190,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "81e709144a87e662c6f2c43b981e80c6741a6b6bb1e0c4ae9486858389471f8ac93d076275b25a3cd2ab9541e25e83a7949db60a844e21752881a2b7fe4cc8e4"
                            },
                            {
                                "filesize": 22485238,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "c44a94deb145f1ea863d046c83f01d6ca172283cdfabb54112aa8759a670ef06454c9d9789ef9fe3101b81c6941e774082437605d7ffe4abdffa1d8a9091abba"
                            },
                            {
                                "filesize": 28388401,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "31713afa8f1ff0341919572bdf2214020466178de6644447474fc8d2bb7d99730dba78cc165483b56973eae3d0f7822dee2da19ea00659135e4d705a1dc1f238"
                            },
                            {
                                "filesize": 3008753,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "a8db90d358bd721d28c3023b01c593bbbdba6a6df145cd952ef11cb9cd95e3af65c3b2b547f13e4aa1ddfb2c18f891631a86e9cde104c2ea8b51f4ae3c432e4f"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "uk": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 52710357,
                                "from": "*",
                                "hashValue": "453dfea0e43ff5feae56e1c24a3e3cc89d346b7b4434e6d14f697c763fa52a615f8dbabec0ded839a2c7ce2dc42bd5efa1f7a4b9690f2dfb48de6bc7c77dd3b6"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 3009023,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "6c195fc550f3b8a20fd5342ae2bc663a101ffad2c7fd86ce2d5abf952725764dd681ef08ce3679e1c71e07f5fddc671415c46f346ca31b96c2e5f314880e1c94"
                            },
                            {
                                "filesize": 28374573,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "e652381567b8d5eb92d281da8915fcf2e110ac564090d0ca0e1f350d3ef1d4e917fdce908578f12dac88a37749458402c7b2295c21375034268c7c39a985c4ba"
                            },
                            {
                                "filesize": 30637510,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "fd4b691f9f84d2c6fd2bd3821dbdd0559cb7b9f04e9631e443c7d3c1b29f301fc282b06eab606b204abfc3b932adebaa7e2f749767388a328725906a12d1254e"
                            },
                            {
                                "filesize": 22490382,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "b3221b25392bcfe714ed7b8a8fa12ef62abc12beeba5297c3b0d9c35dff0c5836e32e1d35ab911459ad82b03de9e760798251ac857a95f97cdc610c9fef7447b"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "uz": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 52281580,
                                "from": "*",
                                "hashValue": "b9a66387a00c733fb0ed6e86a8db4727e8e96499eedb38067b12f399de98ebdd58d9a7bd4202e508a2d3f8e8f708a36345fb9fca1f253848f91b347ddf07cd30"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 3009016,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "90c7a1086e7e3b4e9cc52f3a3e26cbe85215b816dc8f6687de62bf3cecf6bfa4ca26bc558514c23ab92a4e2c4d9a603a637a32ff58ef94c8bcd7863e365c7732"
                            },
                            {
                                "filesize": 28414532,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "9e1d6ff094a77b50cf9014bef984660f4fe372f77585d4856b9b75275423711bf606af321f20f12f845963b7df4825571d1d52debe3f1091530b5e28a2fb30fa"
                            },
                            {
                                "filesize": 30638705,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "86e54620842994c8e51171e3352642630aff25fd943835f4f5249b9407de0ac9255c8e5fcd26e193a72ef5fd9b4e7a0f59ac78c235a19655677d7f04fbe229da"
                            },
                            {
                                "filesize": 22437682,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "8845bbf9a06327d0f60aa67ce8f423e50a5e4e93db728e9ddf63fcebe4ced9ed7d3da1d3dcbcdcf9fda6bb964e84a39cbb3a6f5b0415477dcf52697e07fecf46"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "vi": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 52276739,
                                "from": "*",
                                "hashValue": "ef4566c5fe004e92ba4d6131d913d03943face68c225d0f8007889047af491c7bb1694c85b4589aa32fbed9647ddd92fa4cb8510cd67eba8e7d4b16056216ad0"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 3009056,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "9e7d82faba3c60e2c9c4f5445999a0851305b1d523403fb0bc82e5cb5b8a8632b9d61322eebc77abd50fb4870be53c37f01ec71704be87fa3003eb8964bfa1c3"
                            },
                            {
                                "filesize": 28416906,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "c0c1dc4ceadc1050fa08212f8827cb68931ef5c191fa84215299dd100192ec9461755de914ac7e38c71d465d96138b75144bc03d8e6250358adbf0ff47438879"
                            },
                            {
                                "filesize": 30632513,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "8963a856f2702637fd2d916d8c94af760c871b8fda3e583e041bf5d51a63695b2af493fcc795140c71ee54b647a18e629f43ad22c22c22cb53ab1e0377e2a662"
                            },
                            {
                                "filesize": 22456800,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "798a5a9c6fb517a177cbb11a6bbaa32691379eb9238dfe2f77cf2a4ecbfa5c8d6f4fdcb5d2d5d7cb503cdd3eadda43d52891752cf16491c720defb603999de2c"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "xh": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 52228884,
                                "from": "*",
                                "hashValue": "1fe019cce37bece3a194516f7c384c6fc204e55afaaed05d1e0a7902a4e130f6ed3fae6213a8c0cb62b02926888df3add14f999fb81045cd0cd91202f2700e45"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 22503398,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "7f7769cbd16ea48daac22291a40720018f3246f0102b0053ea1efd19bbc0fef9a775fda0e6ec0413a8819c7cf0e6d37239a73971bec923679a236f6c99f4dba0"
                            },
                            {
                                "filesize": 30677381,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "8eb141ef6c9860a895a2abb0f632b00260faae6bacf19e902eb9534b1c108a0cd75c6885da3483657529c3782e4c517b719b75561734a6d729eac7c4d946bb4d"
                            },
                            {
                                "filesize": 3008953,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "5dcf1eb709f80ce9ac3ba38a2d8561c1282c324fb9de3b1b2729b8d982758e07c3beb3483a020c7d985c9e4bbd22f7480c560e820d012a5dbbae9df9827de0d2"
                            },
                            {
                                "filesize": 28462753,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "ef3ebe3d48e203f3e1a8d8f8be2d8e67ea497129a7ab2ee2f33816a9a33aa24ac5a657e3738ea7c0ff3b4d374a2734255bb3b00fe6f8df839eb78292f9b7a3ef"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "zh-CN": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 52263371,
                                "from": "*",
                                "hashValue": "a0166b9712c5e0c114f6d2423c66d53f7f64f4a582ac5ea61ed486f69bcb54e94d914f61d63ba520237a27b118381b5d6ec0ea59690bc3e5c29f8e5db63be8d7"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 22473635,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "30b7d0ba5a0e18c5e0a9f59c78a2027b7660e77efa9f165fef5f99d39d85b6c9ddab7f237991e81271c6a5e7bcd51852d98813b14f688ee1fa7ead163b735193"
                            },
                            {
                                "filesize": 30595602,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "b839bcadd40d59071e7489ecada6163709163910fdb13292c3fddb265e22bd354cc52706292ec5f75c3fb4b3a67425b279f24d74cb9195f69c5a9cc11d7ba475"
                            },
                            {
                                "filesize": 3008945,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "05958b897577ed02db7ecb91226a94f88186754e25f93997519a5aa7e495f876a3c8ec49a37c3cc3296843dc5a2a0dde20791365ba6cfc9ccb404031108f87f6"
                            },
                            {
                                "filesize": 28350768,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "a57d4b26c940c5780a92309058d2d65456d288ea418df819a35327f403a7e4abd30be07d3e7638131998d97983b680ca6fe8e220289ff016b66f2d8fa4b7a99f"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "zh-TW": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 52482230,
                                "from": "*",
                                "hashValue": "f17c668c954ea5f8ccae155ff562b29b272daf87211cb1a1ee73ad0784ca48e1aaa7ab9793e19ca19d074bee032487af3f3607e3bed110d0b89a8591f6e8d178"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 3008928,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "874cdc3f17084196c7fa4054fd31995a6d3ad38581ddef07bfe641117a15eb264a2a0c884cb2a763c699f0e4f416861db88be4eb3f49c63a4328c88ff96279a9"
                            },
                            {
                                "filesize": 28368938,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "c9d4597ea8e361e240885ee3d4f49e5be7759657a1b4c65867e266f935eef02a6803a562f7aacad99934f8c9276d8b45138f312bd02b173dfa745fa95a53f7e8"
                            },
                            {
                                "filesize": 30607363,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "dfcc5f16880db2a5e0567b192fd98f0168447cc61b4c18588c0c3fc33fc6c3a71bb8cbcfb03d855a6cefcfe81749be6e14279c4aca2800e896c2e0db16d01766"
                            },
                            {
                                "filesize": 22500709,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "6396d3b3376bf4e261a3367533a381323c93538414832b72ed11394444831fb6a8ebf890ae178f0156cfd5b53bf57ca814e11538215ad06cf704ee42451edc12"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    }
                }
            },
            "WINNT_x86-msvc": {
                "OS_BOUNCER": "win",
                "OS_FTP": "win32",
                "locales": {
                    "ach": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53440446,
                                "from": "*",
                                "hashValue": "2c20962b151dbfa50348dccd16a97719fde93bc822912697a46174f58ad4cfcfced80d13751f43c55a2c9c8198817d28e90ddf324cb9810e97b5ca912b276e86"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 29410964,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "0aaa20404d7e5f5fa362f0dfe5e75a9458e360e1124eec0b709d67c8370701f6e774ed40a1e223aef9794568b5da5270f15e73425902a2f8e1834616897438d0"
                            },
                            {
                                "filesize": 21552511,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "3dc834f855594dc9db8aa6650d7a4a3c20eb5ab9f298ccb33611cc3fc6e133c1f7559446441505f3743f23820850bbc32864b943a9d623bdbab4b535ab05b53c"
                            },
                            {
                                "filesize": 27774323,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "0bb7bb4aa31126b4f5f7b56c3d96390e592d61c32e09f5767560413b2d162c3fc260231c205eaad3f166a802cfbc2f16334fff49b16daa13064d96726f1a06a9"
                            },
                            {
                                "filesize": 4711804,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "04869779e1c9201fb1b03dae1031aa56dd7ba16cf6874329f1638239de672ccc2d74d1492c975ba3ef10a5073462435fe26f8f6e39dcc7637257ad4159c1134d"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "af": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53449101,
                                "from": "*",
                                "hashValue": "4a6e4002b7c26bfe2f511e3637743d73d9add2ab164568cdb976a7bd233e880a644d1c2438e8fbe220084039eda6999fb8b2a5501557ccec2ce629bdcb5c937f"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 27714914,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "73508d5d2f39cb532b9a1f90ac3b51261f203bd0f4122ccef6b210ec36e9709a83061e46d7f066fcbdedda861d2d65dcb0fbc0b04c1c7dc186bfb6477d09eb53"
                            },
                            {
                                "filesize": 21504687,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "bc990214af42dcd4037df4fe2fa9c93bfede9b9a48c7c3ba2b09508ceae09ce4b6512d82f45cafaeceb2fc45fa9a6fd1b8f72d18f7b1c99d563f8137e16c8710"
                            },
                            {
                                "filesize": 29384919,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "3faa6186a3dc95ddbb3cf7c23ab3ed659fa9de0e6cf2fe6d1f3c6b52ecc699641ff8f4d0d5a4566df4828496a1ddd7d7bebee28ae2146252f2a756ca914584a4"
                            },
                            {
                                "filesize": 4711617,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "4299e68d8e0c4c982ddafe9e6bc801dedb91f04e69abe2361fcc25eb74437d27f9a22418136e59a493b5632a0536e90b6720153ea09a861f8318d8a462e76860"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "an": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53429233,
                                "from": "*",
                                "hashValue": "ceac93d7e593adca3fabf3524e01338615665d7c135007397f3e206ff0b49f8ac721796951b83fa4a3856bd1f653df82f2696ed3cc4c93257774dfd6f3fbc3c5"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 4711679,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "d83745d3fd4bb6eda98e234f941947c5774272a5947cd5d15589631ce8704cd7419492a0312c20bc643f33562fc08ce73f958223aa93423aeba5d97c0e0efe58"
                            },
                            {
                                "filesize": 29340527,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "0fd673fe0434133748987bb25659961171b688df03271653ed97d3103a96a6bf57de13dd391b316de683064560b526b9b92bd71bf2fd2af844cc386710cfc106"
                            },
                            {
                                "filesize": 27691998,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "1f2d810f3adfe3f386909b4adbc3f1efdb8133cc2e66df3d370bbd83f1dd2d96ce382df54561fbe17449e39de85603f081e490797b0e7af5b8bc3bf86ba301f0"
                            },
                            {
                                "filesize": 21502598,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "5da9bac5be2537a638e6881da9e5e40afd623d6b17ce5fb82cb6d2c8e7c90d36ef63ecfb29cf99328a9de1762e61ff509156172f049d827de5b68f62b26752c7"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "ar": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53496338,
                                "from": "*",
                                "hashValue": "cfff9519b7e3e11efc072e32321c6f016061bab4bef4ade1c3f1746559fb1429d8321ec9be854dd97a07ff9fa9d06affee0d34611da493902569f1efd44afb02"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 29416593,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "e5ca18ae21f1f4b919a03bc3d7ee361aa3b4edc9e0c3622338bfd47ae0dd6896d58b086178474c8ab5786ea1f54f1b62c69a57b5d7871b81af96cb9d5176354c"
                            },
                            {
                                "filesize": 27741618,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "fb271936cc0373b9dc8e15965d5913afae47f7f9a15e1e08663e77a8d82aef8edb3af172852a61b230684e5960dec8fb335d14a7e5368203062a54d34f733aa0"
                            },
                            {
                                "filesize": 4711703,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "a37c49e44e967bbe07d48312d5250d90b3b7c03a87e4e250e1fb3fd86a8ef427c1889ee03622872054a87d424858a9cdbb48ac458631a80a3d8afc6598949bbc"
                            },
                            {
                                "filesize": 21494449,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "47666a2159b485245364f5aebe901b57dc6952a510d7e93d374f1422edbd5fe49a3f51b32f4208c579f12552b8602dd888fba3dfe68c5b057badbd706b5ef613"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "as": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53479262,
                                "from": "*",
                                "hashValue": "4fdf9c21c88acaf8803cc2891a72356f5eb4c765ea3c184a44a3032d575b78d5133375d008a9f86067f3448e7d1980c4fbc0e35d1303851c8e4f9be721240bb1"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 27699113,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "1a2ee29b4b9a8cb816b196420a0ebf5f56c179158bfae4c67c83ce444ff748cb80e65d5b40407eec756cfc6a417a2b8003d875486689c53b19fd2580c813c46a"
                            },
                            {
                                "filesize": 29356585,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "29dd927ccf8a2e5adce147575e3ec162aed25bbe466a928c0a346029549faabd91099ad23f2d6bfbd5213f7af92cde5b9b32fdecb35b88e5598169ffbee0c752"
                            },
                            {
                                "filesize": 4711655,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "fc3677dfac042c01ed88be6aceb8e5d590ee7ed8a7a1e93ddcaa29ba6440a489a7e4c4625aa66dbb4e0912fdcb1d9170543e85e38fb4b5866d9f8f323fb511d4"
                            },
                            {
                                "filesize": 21508145,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "cab90a79377ef3e9bf3a2fb80e3f1cb250b9155727d54e392b84cc99418accfea7e0a2d7348ad776b5c038bda597005b24bb408cb749eed3cc7c0fbf6d59a89a"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "ast": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53368702,
                                "from": "*",
                                "hashValue": "270de5ca323e21508bd43a0cc5cfeb098c43b0283e0316236130c7aa12bb0f8558392eaa56e58f17d0cdc66ce764c0bb3533b5d92a1f08685a8b69bc0d45ac84"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 21480690,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "330692deeffc5c2b3d9b26bc5c1a5bc70ca9c0ea2a352aef432d034d7619019f1c779972e6a6e4ad97494843a6b45b1d8042ef59b48d356a4c55e252fa292cae"
                            },
                            {
                                "filesize": 29293338,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "b960bfe84d52b4d184824497b59fcc47ab84fdb6e188508f2952cce240d09ae9c579b7f71486cc2650b91088d4a0c24cc3eaffadd4d15ec682a11b2bc9bc8ea6"
                            },
                            {
                                "filesize": 27646307,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "be3278d2bd8b55dd270f3b5c0b5576345f69441f476612dd8490a1509882c180f4a2738af313071e50427a6b870945534082da315ba7427c45b54eb3af97febe"
                            },
                            {
                                "filesize": 4711500,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "311140bef486c7f75377d041430732b704aba3eb51ca30b5b70ba0ebc8f85afc72196912d24bfdf30a5781cfb73d6d31bb4b833a4676f19c790ffef7781fc6e6"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "az": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53458508,
                                "from": "*",
                                "hashValue": "7ba9493ae76de7aa4238843415aa88d64d4f18733b7fac1e010d419fbba71eb3d92d769758734fc955f7d87af60d8c6c94725a23d1e805f84e3c1153adc11ff2"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 29413572,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "cf1f486284dd217b00f16f2c128040f00404949f77f5bbe695c07912cf75a44385f930adc1407220b7dc45dd7fc9ec6b276f52a682e1aef2e67abc7be8a41e50"
                            },
                            {
                                "filesize": 21552415,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "7dc4d8f68e1dc2c2b272abafc1889692b3620846b5d431278aea663f6f8108b17ee657b18f305b3aec4267112d9dc33a5d52bcae752587c96bebedacb8119dbc"
                            },
                            {
                                "filesize": 27744818,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "3a7e85eca869c1727dbb3e055843ac35dc63448dd7f6b76f1e7440d31457eee5de6f5478dc28f407af512eeb58ac1c91327ebac60246ba57f1b5555cc6c16711"
                            },
                            {
                                "filesize": 4711525,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "1b95f6acd552dadc19ba688f84273a50a7d34ff53c2c0d4587ae1f7325b100a77b7f4aecf45b6b24631aeb15e0c48c7f5738d62fab41b8686c647e9387863c04"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "be": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53418818,
                                "from": "*",
                                "hashValue": "fabaa394093b8b315f2ec7c779f3e351c7fcd1edc31782851a3bfa2818ad4911bbca91977499ec74a58df194d966a96ebe0655f2bdb1929f691a8008da9a8b83"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 4711512,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "8c005d2ba2e2021c8aad83bbb97f8da70bffb3269e6a47faa2293c9bd99ab560ac43cbea0639769a297950c686ab741677ee03aacc560e412dbe213de83c7627"
                            },
                            {
                                "filesize": 21491243,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "df0dd57e51307569c49bcb5729b259a2f2a089b836b7dc32bded6c075203d2c1b3e454551a80b8606c981d7aaae3ce41129e69990153e46423fd83f4342fac1d"
                            },
                            {
                                "filesize": 27671513,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "b66a7fe7306b437527f5b13e789d55138aa1062cd9c881bfeda93b13e4ca88f2543d42504da9846b38594d46b38267877ba6ac5bcdb96095c92e62b42d72c0f7"
                            },
                            {
                                "filesize": 29329443,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "93755ae43f26893282a2098c6acbe61402f3f4598cb7c6c2aa2581c6f898e8687cd42d577c6928e73a4382f371600955b9e79e1437b6fc6123538727896bae8c"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "bg": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53729574,
                                "from": "*",
                                "hashValue": "ab926df3df27d3a9d66e0cdc3718f7af0cacb6a1043a52ea9f2577d5e7ec139e8e3a78cef2d0266c24a14015ffbbc2f1901ff2bcdb389e2f648ed9d557fea6e9"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 4711561,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "a6c8d6df4d9a303e101b8ccbc17c6f81335e1d1d586053c03eb6c74ce6eb36c4c6a4e4cb92235e258ea0e54312402193d1174bb8041220e1a89c35c8fcd08df0"
                            },
                            {
                                "filesize": 27837786,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "9d3c50feb83d3dd2ca0e2d640bc180ae7feae8976074e960964b6205cbbf483c79b91ac417d34887e6ea501ccc539973adcb9ea49a5f1222caad4b5d6c2d9d22"
                            },
                            {
                                "filesize": 21575286,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "5c977b5a27066d47a838b6cff86cb3202ced6aeecff0b05c5bf26c019a891279d040d7c9372927d628b7405a7d7f89022f9dab433e73dc31f13cb0b51322acda"
                            },
                            {
                                "filesize": 29461619,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "2b8ac7214f9ba6ef9523daa6df3acb92376c5fe3c390db051b29ad2231d3c4a438cd6b525a5329f1072f4934f5c59cc716784d2d677b86af7e8c4de8c794aac8"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "bn-BD": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53507279,
                                "from": "*",
                                "hashValue": "f1fb1c031314721702175c58fe9088c61581a321e99ff0a30b62a858562daf657dc90f8d2ede626454b3a31f3ba1f1bb634266c9d88354b482d70d51b8faf193"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 4711672,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "b6b9b88c73f0dad69a0e1ac8bf9e33e8e39c084c27fe98b865933242a1bd236f51587fe26e9274f229c7083052c0189b84d0006d460aaabd87f0bd45d731514b"
                            },
                            {
                                "filesize": 27917328,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "d15ac33b920674742eb03ce929850e182a436986225b50aefc7c8465e12555294113a72012aa485395a3191628af73ca288181fdf2a01af5f5f9b685eb90cb60"
                            },
                            {
                                "filesize": 21505707,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "90f1a7a25d0d283301400faeedeb6cdc172aee2f8dba2ade3d28c516adca73312e3303da5a2fdd93ca15a66e2ad15e3eb9736624d6a2f9871740769e873148e0"
                            },
                            {
                                "filesize": 29550547,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "c5abf2f2d6749acdc7b0e423150ba8ec491fa71a6c3a974b9b7a72d41c1aeeccd1ad2af68664b1bfd493646c61030c28a806aa6486b706ba15349ced9404ec1f"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "bn-IN": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53499387,
                                "from": "*",
                                "hashValue": "9c5899ab8d93579b1fcdd4e3c8919d367ca58c32b78cf01a91b80b4eeb71df123b6335bb54d5c608ac5a4aebf4a354eef7c1383844667609b39f8faccc770310"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 27852926,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "3b493f970c68069259eb5de1ee388f9ea9887dee6add47d18f3257edaf3aa3ca139b787a7e82a02882e0094544bc4b53cdfd5f7c47ae3687c516a0ea21aad3f4"
                            },
                            {
                                "filesize": 29476001,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "dadd02a753054b96bc93b766b8ccfe77a022c78cb1e4e572adf6ce141d06ba6e9532a4b9896fe7108dd184da5c455ac2f94ee21c9ad82fd0436764bc52c91915"
                            },
                            {
                                "filesize": 4711715,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "487e5f5737d7f82d50a0f680a879f28612dc0f25a41cd1e7f0cf316ee1d602c42e354c13f21edf88cab832ecb40721eb663a9b190872230d6fa9ec3bc1b31082"
                            },
                            {
                                "filesize": 21506602,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "6fe5cff05ac48c6b60ad52930c5d90a5a8ef33846f47e04e8a8f3c6295e5087ce98fd04e9df014760c8c258477d04d42ade2ef522a09dd03d9d1dedab7fe7632"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "br": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 54776640,
                                "from": "*",
                                "hashValue": "620f001983f65580b471f3b15ce43d952bef17751a950f75b9245b7f6727cb1c96a11fb44f5e8fc11277f11c6683d35e4bd798af098a6c29417346bd2f5d4f53"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 4711723,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "83d092a654a34a24e41f14901e81824430f8efa874a47588a9b80be6c14ed8f1a67387b987dbb54c5d485b846965dcf55df111090938e7f2b369886892396e20"
                            },
                            {
                                "filesize": 21490874,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "c394174f9cd3134b04762eec61d07bad14a162146d98c796b0cfebc2bd3be44b77556a739ada62234ff7ee6e66e280680518e217bddbf21f82a5802fa9549d4d"
                            },
                            {
                                "filesize": 29340556,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "4ba098fcc203d15d56bb7d38bc4210a8dc5809cba802a7920018be5d325e3400356b60969ed1c5e7efe59a774e7fe073cff2485bbbab67dba86a51a56fd4e647"
                            },
                            {
                                "filesize": 27693683,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "1e8747ceafbc724bd775ce9135eee44a16a668e3015bd6398d08a2991dbc5b6c23e2b8ab7ae4fbb8fe07809d48bb4335db7db1aefbf4dac6e6dbbe65b5d9e54f"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "bs": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53448128,
                                "from": "*",
                                "hashValue": "09b8f2c5ee54672b1f5897686f56258078ed76be53a8105da3d165b52ab40bc58d319f46f94301a85a08a8deea9319b5cd3c65c498280fa57e208e7b966fe76a"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 29515709,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "abac4f7ed4064d742161fbfb68efdb16bb81220490ecee88c14c3fb39617b372a9fcefa2d1c6121dcc84e947f094db2fe258e79c4e950d2683e6a1fcaaf59a10"
                            },
                            {
                                "filesize": 21503722,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "dca0f682d3231dac0b92bb91b0d5393a8ea54b462d3d99692c6d69e81242a5fd816d304fcd551a91cf5f0710f3eee3777d6a41a86d7643642ac012b247699b95"
                            },
                            {
                                "filesize": 27705221,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "b6997c4674c0da23711c0fc0c116465129b9fa4be0e2480cd1d02339a1ad40b8d062ae6f5b9d194e6fbe8b91ca7e78f9ad12e2f79301b6777a883e17c2ef999d"
                            },
                            {
                                "filesize": 4711636,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "5ee201f9bce6bf3d7a42c006e09328160818edbe77d7f34719caf6bbdb245e5d5c553af257131ce455390428aee7d3ccbf41b5b958be5306e76a72361cbae065"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "ca": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53830294,
                                "from": "*",
                                "hashValue": "7ca5ce5838cc4abd06d1678e7f492961f42350d8bd85161b6c042ebaed8bc00e49c311bd05b19da99a0fb71ab115d18b1ba24d1e1c3ca4670d734af738017157"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 29383172,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "498a019b686609e32270da1f03b5de76cb5e9b936005b607af4ae6cb3cad720ab33b4bf4677c138a0fc0e7120036f2fe17b792cbf5ebfde1263239278eeb0703"
                            },
                            {
                                "filesize": 27731898,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "0fd2938b5d8a01dae5f1e8143b0c54e4257531da4578352344d5246cf6a7a57fdd3097a32252559bc21f783f8c5774aed6e6abc51e76e35f656f86fd9b799318"
                            },
                            {
                                "filesize": 4711740,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "be1cce7571c96c8c0acd58125389825e9d7ae7d6e46178cc88ed6e2f406e1f57402123932b6ee05c07506de240847c8adb5481032fe0b371d4a1bfef0dd724b6"
                            },
                            {
                                "filesize": 21529556,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "cac2ef7ca20db5fedc3cc59f930b5eb9c8ab049e05ebdb9990d53c7fdb03628e732ca470f80c5d730bb77c06b94338d1dc09864a4d59a97787f1b1e4a0cc29e5"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "cs": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53415641,
                                "from": "*",
                                "hashValue": "db4188f77fd8fb23696bf195862c29b50f90329c10a73a56ee69fefdb43d6c2db7538717daead3d510c8f9515b0723a22bff65f84866bec0760f274bce45fc5d"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 4711683,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "b1c87f26656f4a1e9ec0ef67938d11b50cc24236ed0bba2ca0c5587c8d5979192db2fbdfe45e48559cf3d838b9c636dc7b73923bf80d86c345d7f60216eeed34"
                            },
                            {
                                "filesize": 29385426,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "bc969ba2ff1a0e3f12a4474725a956a35e24fa3d24b60872a218fbfd1d49022b152c981a1f864eabfd1dc09272c8c55b2637b84a479c229a288500d92fd8e3d9"
                            },
                            {
                                "filesize": 27711334,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "106008ac4330095cdcab47b0943f791a3a5dbe1f7101d1ae93070f09eed43cc293ecab8ef5694204d62c361abfd064c1f400ec802d32cb899b03c5c5e04f2e6e"
                            },
                            {
                                "filesize": 21513007,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "edb45cf0bf2ec479f12814fab4cbda6a47259b7c2c56b36219587de62c571a2021f7fed27b750831894c7b7105ab0aad0119c411fa4623c4ad885d382b8be447"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "cy": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53410201,
                                "from": "*",
                                "hashValue": "a65d564d1e9303d3c7773887280d67072bc72c300626f2f1b3dd395dd06b673845700602c634d3d7700c1454a1172ac72088942b01fa26e6b11fecaa6681ab18"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 27689953,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "534a9341ad29a5e0749b79037073ed9c9806250f9409a369dc581489e4f349f5c67aff8c6308fec53fcf578e2f116a426c4a86b8b34fbcbe717016c92e5dd150"
                            },
                            {
                                "filesize": 4711669,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "4e993b5252a06b25eb51b1abd8d5513a20e7b8b0bbe712a2a9d94418d5069b5c29ac0f0ee3d82395c1511ab73601388eedb7727c545f96f0cd43f46e9f81c5f6"
                            },
                            {
                                "filesize": 29348945,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "c394c36519ee9ade3e5dfcfc91e2caa1ee1e7f796b56bf72bb047dcca1fb0bccc178b9865e0c2436ca62d30e4702ffe89ceb8d3d1afa0a4f0c6b2ae03ccc3868"
                            },
                            {
                                "filesize": 21500846,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "af403137666965dd0167b1ca54a88e76aecfc934a2ed2ef8e0c2f2eb2dac34248bf4f062a6e1cfbe81de3c3d84ccfb720f87d0bc58fc27045e42c1d982cbc790"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "da": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 54042066,
                                "from": "*",
                                "hashValue": "53a82d4d9b0e88355f4e840ceba02f4363fc1d28903658bd014c1313e4fd882fa5a3b13c243b80d27fb8ad7169e1f2aea182181757ebf4843d1bcaac4891f91f"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 27673299,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "44573a4c1b6ae1320287d711a874b1104b28dcea1203fe27852417b2ccd29da86899cd667322a3921f535aef38aa3d232da85ed1644cbb7db05d3fcacadc9330"
                            },
                            {
                                "filesize": 4711675,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "6e5434e8b232107ae3fe4856f90ac69861786063f9c43d339c0bbb026565d32ae77b383e6e898aae5b35741f47ba0547997db10c0fdce4fbf6197f6ff4d8ec44"
                            },
                            {
                                "filesize": 29342430,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "5ae08b311109dbfecd5d91e77307c69a6684102c80a9493c96535fdba3e6d79878697dba1bfaad4da7f457c9dcce662c4e7f13965292d3eca6a027fe7f72c6cd"
                            },
                            {
                                "filesize": 21491613,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "419d37324222c3e6243346880ef65cc41fa01f761de029d88fdfd325491c21159bd9577bd1f5786f3ba38b260f7e5cfdf18db91a67de7690481dc6f49590d019"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "de": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53419180,
                                "from": "*",
                                "hashValue": "d483c502b8636e0a4bddb6ae4085173c0ecbd7e37fe13c7c5784d896e253e111018f846ab70e264d6b9d7d0d7bbbd0e4bfc37d9455080ad55df949fadf66952c"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 4711643,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "aa4a0be0e70d356504958af9008e6313a7a4204a5083316c22c66477da50e5893741cabe68cc6edb9b5f8eed5f03cfcb4367465cac2c5acce4d3904a884887f3"
                            },
                            {
                                "filesize": 29347648,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "bc57715556e68926bb7c6bd2ecebb6a8495660f67f41607b3af1e26ecc5256f97b3a948fc6faee696880fcd28916972905c120ef3097684de6edd5488a1825f0"
                            },
                            {
                                "filesize": 27690490,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "751ca0c11bde0d9549dccd3f7d475bc26afa37eff06281cdd54fcb46e418df0b81ca2bdec49e6b782b256a14598b18af15db1c91c72e02cfc91fbbb0d07aba5d"
                            },
                            {
                                "filesize": 21501675,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "32e2606171bd046283d5b0c217800ddcd8259b2dbb430ec278756fcdd98fbcfd6eb1b78c0702cf0977c26fd6f5132aa36c5d7784348e24d2bc9095425ddfc1a8"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "dsb": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53439426,
                                "from": "*",
                                "hashValue": "d45aa2a22e2b3cb5a04408ad57dfccb9a1fbd73137fa37158cf5266ff97cbbc13ac6b127a174e1ec1dcf89e18bcae1bd0f9ece9b882b10963450626e24d8d1c4"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 21505307,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "990dd6d50c87a92ab69054f6e10f6db8ecb04ec71333d864d80b05cdecb99a3551c0925c3b03407f5e6a244890b35d8bb224a6362d1a323d6eb84e1f787aa9ad"
                            },
                            {
                                "filesize": 29354035,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "8b47a67b8da46d1fa46910ac2dec0cc1557cd5a82d11266708007a0f1f26238baed21f948b2ed34c5f8078fd58b91f30c45599bcce1f33e455b532d28dfa8239"
                            },
                            {
                                "filesize": 4711702,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "62eff408f072f2fb312f9605a0465e0ec69648cfd8545b67e25b1ec38cd7e36286cc08b98ab6ca82ca39b39e50f2bc2a9007a944bfd7f8a7ee206c903aa48fff"
                            },
                            {
                                "filesize": 27698942,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "4996ae9e644be50750a966d127581d39c067ad7a1f0fa043263a32b9dd34bc1475a0a5c0b38d71377e9a8c1d8e6e4ea4c1e4dfa3b2f7197ac6c36b4e67051f08"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "el": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53464969,
                                "from": "*",
                                "hashValue": "9851f4de7f5623d4689175a9bda739ff41b6463c32fbd124123011ec17422cce6572112573bdcd0e8d3e7a10085343d7d3eabbdf55b60365fa8d12ab7ecdb2b5"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 4711656,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "c1daf49e75c340dfbd018a74c93e66177108628b277cfc5e85c781177e234db621f0c6e3c3c9adffba868ffbd8f20656d4ef8aad03f6439f7c2dc5ebb02370db"
                            },
                            {
                                "filesize": 21498812,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "5f38caa7a7da4b5b74a128fafe44c4c75cfb45d522751d2a81f29f67ae7fe0745f58cf16868506981b9fbc18c206a8ec6f5630a9cfd6e0c317a8d093210bbfe0"
                            },
                            {
                                "filesize": 27683461,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "0631cc7e2ce13168005caa000aa3d3659312e3dd571741fbfa88fe6ef6d27d43e75b4bfc0471a47da88f59925148b2cd34e3bcc44329355f029c43be2859eea6"
                            },
                            {
                                "filesize": 29352087,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "1f5dc8eece4720f8e5e00fa00d2ba8700fb2cb908a59ddcd682bf889d95a91b9b841a1b8dee521e5b4788f5c647b5c44fd42a9b6508a6c40734bb9e711c25802"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "en-GB": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53400374,
                                "from": "*",
                                "hashValue": "d4966e16272beb123b8b51ef6029438c39a892deb893629aa51ab7de4ede99d4c1dfa6977d396f7c82a4b85b4656820012033babc3daa22f556241cf65ba9e9d"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 21481628,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "8adfcb64498e7f0cef63df27e58b543ba94836990ea5db820b7405ef61218ef670d26d12010e61065d79eb082f248147bc1ee08c826937b167cfaa1b88aff3ee"
                            },
                            {
                                "filesize": 29321777,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "e15909294726364d04638d690c25fa656efb8e27cae5ef2e9e7f77d92814f547b2e52055fb74787fff9f9c02a73ebb2ef0949204a5accd6c98543ff1dcff2f53"
                            },
                            {
                                "filesize": 27698574,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "ba72467b63e7a97dacc0c929899c70640a7deee90ab9a5dc865b006a46eccb5b26ebc70428d25e58065b4e4d0056bd33cde1df0f0a7a631a0dde5b24d622524b"
                            },
                            {
                                "filesize": 4711431,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "98099129a24e610d61f6f8165d0639166bd62e87728166e9fb9ea757dd8bc96a0195dc47798e69051bad2f4448650237372686a00db857f2eca256acecd9c855"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "en-US": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": "53676073",
                                "from": "*",
                                "hashValue": "7f54164546d45e4fa4c984b4710b83bdb502f2c626318c5f1a2bd9ef16ffd3fca004b805e6c36a20df5dfaa444031c8c531934233ce90a3b283863806c870b35"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": "4711762",
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "34e08c89ec8788554bb28c6d487d17d8b0842ee8ff30562a79bc3d4242280f666a6c12167fb146fafd3a9a2981d7bee2f329176471212f5d2e53290b38f9b1fc"
                            },
                            {
                                "filesize": "27701906",
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "0aa3e27c8043bda92af5b9720b10171d0b6bf05445c300f2c66d3e113f8a96ef5615fff883db13fe0d40446348229f4a36cacb97e79a161818ea51edd70085af"
                            },
                            {
                                "filesize": "21513098",
                                "from": "Firefox-42.0-build2",
                                "hashValue": "d817b11d1e7b027cad4f1d5ff86c5a4e460bea301fa7c5897f665470dcd16c03ce6e2432d93dbd202a9f879c74024bafa4bdd4d1c3cb5d530e7b9c401dd22131"
                            },
                            {
                                "filesize": "29361167",
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "bc4193e0d38ebcf086a6f9c2cff1b7f342b482ab920a83e3cd209d94735c2a5c32d22ba60dc4688f16b93f36de32a09591ea85e66bf90b28877718e466bb5798"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "en-ZA": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53405401,
                                "from": "*",
                                "hashValue": "a6514ee45b9e86f63b4fc09010ec7782c932f74d85cd46d8efcc3703861b11a22a924a2ed715b720960f79d51da30aa680cf9299ca9d0a2a6a4e32e0e57bf952"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 29323318,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "1d9f58677d7c027a84a9e4347e4c418833712f45ecef4373c219a748ab619f29e94fb6720f54c908faebb0cd520a42b1568afee6b6c917b6cebf180386419e7d"
                            },
                            {
                                "filesize": 27674552,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "fa87b47741fb69d3cd9c4a08271cf23078a60fffb9e32430f53b40e0a4813b5491b228c3f4e0e5c002940005e0f711432b531b73cbdbc609eb9d5932afd5c450"
                            },
                            {
                                "filesize": 4711458,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "3ef53cc9544bd20dfd2360027208a152a9f7d62192086150298d22fd25507d8bb9543470b5d9e2b0c7121debcc1e664a743f62a8854a549b53a40fbd6809e13d"
                            },
                            {
                                "filesize": 21490399,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "2708ddca362c7c4af5f80959e637b4f95735310f7623ec7e64d80d6101c7630e2dd49d76b8296755fbe148a10da7b9c23ca5f0c395f9a132d10a6c0e932c90b0"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "eo": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53450966,
                                "from": "*",
                                "hashValue": "998e5c60114f7d2d5f18cf10b7141a94bfddf265037b92ecded4494810fb8c3b28c81af6f8b71377e0f2bf049641c7f019bed9d2f899df003d624bd689e9539c"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 27697707,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "a7cd9e141671767e90cfe01168b7a1b66b8303855d67d3f6d58b647a38bc27a683c83278f355d397c2a594293802287834401e94426666ac0a3497a4ab719a06"
                            },
                            {
                                "filesize": 29365753,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "fa15ce359481e9941e387a964c47b3f3953da18cd28fea2422efd9b2a00d5f01ff49eaf6aacf93446009e3579cbec6f402c5fc338f362f3404d27af0aa09ee21"
                            },
                            {
                                "filesize": 4711445,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "abcddea9b83d5bac9240a74888356229ac3a188f7ee8c785ddf425fca8fef3ee3da5bcc217ec951ac55672265340ee1f398919551ea6b6d78c5091de4ea1b7de"
                            },
                            {
                                "filesize": 21506855,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "5d9292b3d63d3f0294b6843dc77e78a24ab2829d66593523762d54d09aca4f126b31149138fae3db48ffa171c532651bd4e6ec984b7d2b4886ade8aba8f551a2"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "es-AR": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53415730,
                                "from": "*",
                                "hashValue": "a56768d555f4390257a7e14025e52c6cfe3113e1ccc49c41441dff9070ae48f7b892b564263d4dd800018e601ad8bff95cc3fd1d0b9f83122adde5eaa152c660"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 29343866,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "4e4604a4f938dd63c484b32c5115ca4dff9eb481edb135ce3d53446c08d0d1e37ea093acfabc85b78f4043f2fcdce31aece069eb9c54344bc106fbb4a13f9ea2"
                            },
                            {
                                "filesize": 4711565,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "62edde93cdcd33f8a645c0f4abdaae6f6998f4ddcbd46db2fb6b11e99fb1d80b45fec73a947145e89a8b30dd17ebe76fc30d5e6845aa1d2ff11022be781cf8af"
                            },
                            {
                                "filesize": 27687156,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "35e4189f3c8aa911c039ac33f308902a45e2fc16e6bcff5eee48879e527550ad6103aefadfb1ca651917486dd01dc6c3c9c42208ab77c0717c657b2f031dfafc"
                            },
                            {
                                "filesize": 21498589,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "aad25f24da152f385ee083fc28cab694b1f30aba9474bfa25cc341eb5bdd6f5016c72a024c4ed1d201ee1ecc7515f1c764b0002bc90cb7fd41a010c43bd51f63"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "es-CL": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53340212,
                                "from": "*",
                                "hashValue": "8b2709c94e814d7585a3d2951a056c71bdc14f2857550a9f6d5bf10db38b4f1aa89c87179ec4af89ba7e030e9406452376c34454986cbc742b27707c95596419"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 21469173,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "2d50928583f065a25dd1bf29feec3e33de95b5e351ce1c981283c9606e1968f9e7a3098c09b1b3da0b1307a318b0ec90ed0de08c54cfbecd90625cbee161447b"
                            },
                            {
                                "filesize": 29298593,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "524c5e2e1a5eb6b8def891ce5aa57486366e305b67176fbd3eeabe062047edba4fe104335c3035c359412545499d23db2bc08fcfac0a5108a73a2f03ab78d302"
                            },
                            {
                                "filesize": 4711553,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "3f08c113c95895468bd7049603ebfebe2513620199b1b37117358fb647a576a2988b0e7674d752df51c7eafe20e85423f35a9de1db147c56ce49ced40b3b3797"
                            },
                            {
                                "filesize": 27655018,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "0fb2c10518e30d7fe3bcfcd4ea33e40cbffad973b1e7df2913ada631315c37fddeb1235862eaa925eac3da50c611126f06c78b61339a00f8a852d0299f5b4dda"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "es-ES": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53327045,
                                "from": "*",
                                "hashValue": "94038464d90298c5ce9a0e54ee90532000bd50182f61e4cb6f7ea11c5b8296591a9dddb1af78c8f792a89fa2ea136b2fe8101e544fcd154f3bfe8cf3fd42bd53"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 27644662,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "c9b058e02c7792095b6620f86d119069aef5fe4ec4ab24944c3d20bb294cbe42a1df21d249cace4de1eb3d7eeb0bf85e91f9973be0908aed88746df2a4e97b8b"
                            },
                            {
                                "filesize": 4711564,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "459474788f1ee5fc3d353271159463e96438b3516ac76c8b6b81fbbeb1986196f269c71bd9f4911452ffb659654b54cce96315d06cd2a0ac72eca5a8f498c54c"
                            },
                            {
                                "filesize": 21457347,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "a0365fbdfef9add94f343992569f1b133eb1d2458903087edb27748a2e4ad40398808076c1e12f4daa42cbdb12c8c04e7f456b8145f5083458225dd3492a08ce"
                            },
                            {
                                "filesize": 29287036,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "54f16f7445ce456159f755b3f949c9fb793170652df68fb657028ab254fe4a0be97803d9cb7c899d05781cdbc5bd4926bd80f210a40e4ab0872d9e157403a8f2"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "es-MX": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53423376,
                                "from": "*",
                                "hashValue": "7dc6f985b8ce54fac2cd7a6fb9e046e82d4ec4f5b80801826449ba76904435924b27dd826315619ae39af8af173e420e839fd47c2da1c6cd9212734bde7a5730"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 21504592,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "f862b53b1eeb718fa016d3472cb31039bb0600084fd3a18ee734e1e5727c46e042d29051cc47c16741ad18b58f1dac3e0860aeff70685881e7213c753a815fd3"
                            },
                            {
                                "filesize": 4711470,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "b2b92ea9715cd60f9c69becf72bebb656de35d4671f1c6882eba07b5cc1ca1310ab1b27a7492dc45a4e55ff366e4e3e3c79d3fad72ca00c86016817f2b826832"
                            },
                            {
                                "filesize": 29392979,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "9b3e4886a1d58712d7f5015b8f5322b0e9120188b9b2446c7d256ef89a9ebd93cb8ebabf8e217a728ea31537b32b5e8f768c49771be88a5492187849e48033d3"
                            },
                            {
                                "filesize": 27691619,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "e3d06991379ae0cc65ac1575d563b67e6528abcff8d9bd3d1e4dcd3d2b54316ff80a4a2090bc17c8db351b1bd802bd0bc68c6a6bcfd67678a0f82d7214fc41e0"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "et": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 54248063,
                                "from": "*",
                                "hashValue": "a813b75b7fa074dbd51bc9d3bdcacfe84003001d0985655ae6f4b676a09fdd2eefeef582a88b6b091a8d6501fff3055f7b383ceb1b0590c5bff8614c43ff4272"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 29334748,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "1e37c174776aeb69ab10b780fb2c9008c633847cbe33a7ebbc6b423392fb4a3182aa4e8a41f7e1f4a5fee41956eca2acc0b2eec8a6de4a03de4d94ccbc09c368"
                            },
                            {
                                "filesize": 27681280,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "b54749ccccee49b2af2da92e7b3e06ff2d6c3273233f7e92e84c78b5a14a3b51e1817e3cde0265c32f0b1290f27b32011d30019cdcb7a76a5cd476de391727a6"
                            },
                            {
                                "filesize": 21495415,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "ce0b89d0cc0e4a34a6b2f8b2f52d3338cc35de1778740973dbc4dc2dc80d3aa70af72ff503fd340d0fe422285422eb8a18fd4b3adb689476dbc3c2dc38a7f19a"
                            },
                            {
                                "filesize": 4711678,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "a727398c0f969f9918286d240273b0557089c37ba2aa3c715816f86c4a687b86c2f4dbdee6e243b4b2d0fe1d1d25a70a4f1ddfd20624ad7f0135847428265af4"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "eu": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53433670,
                                "from": "*",
                                "hashValue": "49d1c9adfc951eb0beae4ca4be117da63cea520248f7cb2d8a4df0a74b7e46580d85b4be6d30ff641131f3c02068d2ed7022126606aff89b7e38032b51397ceb"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 4711492,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "9e19fe9bd21b898b969c0f6b7ed020bc56d9400436b90a9d93e96b53fa4eec77f88bd4822124c6ee08317e5e453c560213c25b45f6ee38100a0184c3fbfb30b3"
                            },
                            {
                                "filesize": 29381371,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "73a0140be0737cc055c36e0dc4f461bc9c9ed961722fe11653559e30bed266855f105342d0dfed3c66be2ffb395a388b1d757cc4807984c243d8fb9d56482ddf"
                            },
                            {
                                "filesize": 27714191,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "3eb22c8ce6f9cff3089051d02336b82c779b85a208d6a53a1ee823b4fb75cb1fc412bc556a529f0b0006b457f90790958ce77856f3a11513077d3d5198638f9b"
                            },
                            {
                                "filesize": 21502654,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "d00ed3c5f80f73ec9a252d2ac9db400fafb2df27581b3ea510fb096fe41bde8d11b6b7e40206f76aba99764d3d262c3cde8f880c46e0361515932387604aa931"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "fa": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53493894,
                                "from": "*",
                                "hashValue": "7e1534ea69f164ce87c86726fd0c57056d63efda6c76e1d5f83ce28217cfa0988ae5824578bb7e19e357d98fcfd76c1aafb2fb3a619e208bffbea45fc4879a41"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 21601634,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "4b8960571356f9baf552f97e41c4440a618e003d33d6af2b20f0e54d20dab908c48d21b5b3cd708e1757b52f4a6174ca2a1650232f94aa02f47ee006b4243801"
                            },
                            {
                                "filesize": 27847499,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "9da2e849ed26e73b5603a57b9eca2b24b4bd40ed7be97652b1c2d58334e3162fa88d914d58cfa67185a9e8db44d56c445480ddac31bb602f3d87d4adf7ab6a7c"
                            },
                            {
                                "filesize": 4711481,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "3d5662c923cb5d7bf14d0a591c17ac86741ea79d230824826db80a31ded77d723200a1b0dd218236c01d0759455714e31ac67e0f5c838e76b1e5d928db2a3fed"
                            },
                            {
                                "filesize": 29482814,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "424b38145bae26eafa06741b6ae6a10e30f116e3cb517fc943379a0f71118f13f4327610e4f91e781dc09ba28fff8ba7e2c4f932bf94f6c3adb2e6efeb73675a"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "ff": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53421612,
                                "from": "*",
                                "hashValue": "c527ac4ca0e6b3d6abc79016af975e063cc424f94b0dd3c0e7b8593f0ae3b162dbd4f42c272e3cf279f774c057c49fc32bf35dbf1e403b95f502435630104d93"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 4711493,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "549834ee68925e1fff8d255c9f9331552268e7c520aeca6b85adb2201d911e913e660af8d70594795dfbe3ce268f1d242e03bf66d4a379997b3669ffbcae12b6"
                            },
                            {
                                "filesize": 27672724,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "1c1afcf7cf7a81b99b0f52d52ab46f0fb60c02f81512671814036182658f75c2d2ffd753c3e207e9c30d7bb796fe9c89025f49e447f802520d9b0b72bb567eb0"
                            },
                            {
                                "filesize": 29328589,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "9abfb39b2eece6b84c29abc64ea54b801b92a8a04bb9c5aaed4169459a2bff4b47cc4f36ba6351623e37848d1b6c9748deb588faac71ffd82814a4b4a13bff7b"
                            },
                            {
                                "filesize": 21485188,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "c0b2b10a2b0dc726b203c1509a11b39059599e17f95dea77bf44f00c9ea5e8e007a0282901fa97d6a6fa1a2abe6abf56b979f3b6e24cb3b744e7e1f66da549dd"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "fi": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53412156,
                                "from": "*",
                                "hashValue": "9b93b0c29ba5c3b1eb53cb499d52b4408a198e62d0be16b8db72ee2d5e9a58d03818b55f102e0d3c65341cda21a71778610da8cf1a4018dcbc33c392c48ac3c5"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 4711488,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "f385ca1b92a7a77c37142d0d13fd1b807e563545d05d32a803005ebe4906c27424cc3a929328df4258dafa4df5776c220603e068f92b9b5740d8c67b2930d66e"
                            },
                            {
                                "filesize": 21492613,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "bc438c422fc45d301dd20b472a875fc3d70d0ec4f30cc870d5527abc892a547778342ae3b5ad969a336b0c458339addcc0ebd8f6b6c5a51cc02efd4f0fd40fce"
                            },
                            {
                                "filesize": 27678304,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "bcfb5dc23fbb26e7052aedf041b9669a2297ad330cae89031262c38b9dc1edbd1d900161b6a84a10feb6d0f883769ea132f420382238e1eb949e5b151ea39641"
                            },
                            {
                                "filesize": 29328599,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "a1b7ffc814955184d6231e73be7164f2891ef9e000581b788fbfd24d6db762fed5329a11c544f05b551d7a38634144f3bf3bbb2e8ad0bc251280f908b3d1a292"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "fr": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53793156,
                                "from": "*",
                                "hashValue": "7aca8b110b21a8510a5ee4d0947b2c630d277aee1f80c51d943ccbc17642a320e486194d3115c80c8e4fa80c179a9ffef094d33ebb069405838457f70383698c"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 29369474,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "12321aff2f7d811a6dbbe5be6a0bddf445892d5f6ab6e20747f3d8ff9d2ae42b508ce1217caba779607ba9c6fa0c8adba7737f57a718fb0e5e275c7042761577"
                            },
                            {
                                "filesize": 27713464,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "6a5a2d3fbf81bf4930aa08145a27cec96b7abe4fea05ef253775efc6124fa3b6711f4ed28fc967cea53e03d6c8bb8f54f14871cbd43b40d48bb01a3ab5c60726"
                            },
                            {
                                "filesize": 4711471,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "3dfc85763dd44748dcc301bdf62dfee4a1a4af696cccfcbd105d3ccb2dc767dbb289ed7ed027d925fa8ea2c9959e5cb849b353514dd289407547cdcb4df4e681"
                            },
                            {
                                "filesize": 21525903,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "24e49ca7c748821906adf071607c1a0e85946d144b5d65fb49b830ca427a6142141ed273a96a994603cc15e85f3a608e0bad563275c049a941d8d9f2e2a5def8"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "fy-NL": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53420892,
                                "from": "*",
                                "hashValue": "0b6e11ab340ff9854080b6655b39110b6f568a112b4da7e2da09883d757f5e62ef835446a5db5e4ee0ffec3a230e240c5c8da15c37b8e5411546932cde1ad059"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 29349784,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "af9eafc680fa73c5d474b0a01f16a443683c59b13a45312cdaa77470e6be034b2fde61ed48af2ca91b654cbc9ad70ef307626ca8438364217bf12d5d69e84083"
                            },
                            {
                                "filesize": 4711440,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "c890cb3c4d8f9028f76fff43cff388f679841e3c7c2a6fac99d781832dd73801792dec0d1d2def7dd009b9e79b40cacbd2705a796bfa4f3b198ad0dcdcc7793d"
                            },
                            {
                                "filesize": 27690786,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "381054f2bfca1f50db92448f02f2100971fd7a4d4b10d9b25697d6aa483184bc135a15e257f7f91668a92189a993adb71d5aa9fd3a7e1f2535ea6df13a0ab18c"
                            },
                            {
                                "filesize": 21510776,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "adc307b82db8b7c23904f2e8ae3f05e6681720d9009879aeafd995e8d71e10771190f6d4659cc4df68ad08c6514efaac364c152e6070ae3b029f60925db4b69f"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "ga-IE": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53433321,
                                "from": "*",
                                "hashValue": "583187fce39722f0577eb785156da411dc9e365d4a5828ec8e4698358c89432a6b938c3874a8e366b0e7665b80efc4d3fb98b5827b11806bc37948510b530415"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 21509638,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "1bf6770ad3dd4c8c478f6102eb33e9875b4d5551f1d44c46e801d634eeb6cb2b0ebd5d6b997f9741cc2a0b13c8e56596f65cd370d8ea290a78000cffe841794d"
                            },
                            {
                                "filesize": 4711461,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "6b54d3b141e2117510cf5ee665adefcb54c1463fe7ef85041c1d81fcf0efb963357ab912e238cc8b6928ee64426d079948b4356a4750e0275797dbf3773a5724"
                            },
                            {
                                "filesize": 29357517,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "15a966c628f107d7f7923a48d0988b309913720fee7bfa8f9b2061053374734626be90f4ecdac3df84321a0b681aa7911444f7c11357d8de6ea18dd02c755896"
                            },
                            {
                                "filesize": 27704243,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "2447cb2663a9ed1adc5e343e7c2e5f2c45e7b71f02fae7b7b32a96489d2a504a18946fbcfa02ac2255b0de2ab4faa1c5158845cda09b0e41d351ab56283628fa"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "gd": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53422831,
                                "from": "*",
                                "hashValue": "3964b6d6393e55c354eccef98fa814b916f09a02372873ed5e0fa1fcba9fc6770cfd0a20b1a0b3c4e0ba27075ff8069042cece81d4d6220586bbe4ed9c6315e2"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 27695366,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "a3d1bf6752c097c547a17a719d01511501d690c439bac566d50d7cd6c4ee8bcb547b48aeae484f8b4ff2d35cf80c28cb2dd75f085ce173f82e340b16eea6460a"
                            },
                            {
                                "filesize": 4711488,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "e6a63dba93911f18c75fa687281d7242cdd2bb1af210001205619d1b58f7b1ceff751b91c57f35b0c2ebe70f51a2eff0ccda54cfd60f40991f63805dfcabd5b0"
                            },
                            {
                                "filesize": 29345542,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "64880418d2435912e536b1b154819cda59cbef7643d0bcd63948171036c757d0793cc6d9e363ab24e9c9d2fa67e852311ddc18b7c9953eda5105292e2348df92"
                            },
                            {
                                "filesize": 21500037,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "18384172915900fe86ac7feba753470946b9d846dcaeed0981b757d25cf932dc9e145643d763ea6ffbc7869b55476a3d1c0f975b33a92ea15fd2193425011265"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "gl": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53409964,
                                "from": "*",
                                "hashValue": "dfa192647a972c1eb55d42c8e7a791005016c5093ee954f36cadef93fdac9a012a291212cfcb90f345c1b762361f852391abf2cb39531805c62803ecc8ec126f"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 29421898,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "ec0a7b4243434c77f3e36ad949ebeaf84dfcc38eaa1157b4013a366eb5e898c2fe357b8e43063bf40b4909a2e870add31234b4ca05a7bf9e3d28c264cd75edae"
                            },
                            {
                                "filesize": 21501263,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "064d89b8f9068892e2c219fbc8f97f20a9f661882fd8ee0d53df2c75d56a4eb8a1bda313e753eaef37d5c729d5eeaba97de61026056a5d3a64c4b9e6fee8ff6a"
                            },
                            {
                                "filesize": 27797613,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "8278f2bf32306e336ecfb276039d11b7070ba7ba4b22133d5a44c5f1df0d37807b7229e2b0b6c9b070fd4153f827a911c349c6d46d4b2abe8e569592e9928c63"
                            },
                            {
                                "filesize": 4711686,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "63a49e41387a5fe1149bf8485207d13264a2872c1e5d4084ed49c3145ab7f01f547475dda03f90119c875a6ee1e16bf792616609cfa1fe529bfad05a933b495f"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "gu-IN": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53451416,
                                "from": "*",
                                "hashValue": "476b82c1929a431b1b279a6207b8140d09edd40398b48cdd697c34f90fd825772efa0a8680d9dd36cab4cc6daf8d605e64e4f304fd02f6c4f52d8041975286dc"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 4711723,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "6cc872fee473af718abf7e2b8df086dddd1156aa86b132c9fd9cbd49bdaaad66ba2eb8380749c6fe9e4c538aca17ed434f32b42c60426bbd52d8faa2ad157a2d"
                            },
                            {
                                "filesize": 27670091,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "5b4df3648b81b18459af3d04024a73284e2bd2e99c4ba41d9e01815c4a8b47dec46a7821bb787d3c3e294be459a9f1b3a762bde04b6b361ef5897650a748f06e"
                            },
                            {
                                "filesize": 21496042,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "bbcba78d92c18042034831e25c35ccb4bc88721b99fb5f4a1d9a201e3d73b49f1a0f8a95a812084683f8276ce2b6bcd1fdf5d30e3c3e49e136742e9c6b9432d9"
                            },
                            {
                                "filesize": 29324358,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "576bc084383119953b1fddd999a9016202ec50417b138d70f671459333812437fe2d252c349e2baaf545027212c869cf67c6cc647029b5d110902af33373d94c"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "he": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53447523,
                                "from": "*",
                                "hashValue": "6ffda38a1f3c461811328d84ecdba84fb5751fc6072f27c038df9cf7c2b1ab0d5de487271f0993ed3d1bb816e9aa6be280d3b36b36646b02cacc9eb4ffd450a0"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 29483510,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "fdbddc5bca164d0b61e4586e5d422d2f7c3ead68bafbef9c19f2fb320aa06329de24796c12bd66b5abc86515aaf95e4593ae013a3c270036f8a98b2eff093cbe"
                            },
                            {
                                "filesize": 21503772,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "abe012ed89a9ecd3c5df61083e34a0057531ea89c87ffb802f53c1fa739f1ec7b11054bd88e8d3e25b49bb1d66d97f2e480ee0f95e83cb29ce48625be2b6f9d1"
                            },
                            {
                                "filesize": 27844757,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "a90638575cc4930dfdeb6408ec95479a4e9a5769eac33e1779c3c5a1900383a996163f2075a793b4d6bc5751ab33029683e483468d130f522c92ad7476667e19"
                            },
                            {
                                "filesize": 4711653,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "81e43c1f29f0ecc9c3ac67ec9db9e9613c906aeabe5fd0efec5e2186731ebf54e2694fa79cf3d7c62066d1cbccddc51e9e7031b4612900ca5fff25c85c1d9f7b"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "hi-IN": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53474125,
                                "from": "*",
                                "hashValue": "6d2600a79644450f06df983d4acf94edbe9874d186884d03402fdbe4c741ecef956126ec84ef945bfcdeb2585fa94c527a162aec6e99acd0fa959817cb85cd81"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 27672283,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "87d8eb54de92618e6216e1880f241d00a71778b64a660ee319bae9187598dd6682b4da64679ab1874be48eacb7d319edf3c9b49b14eb0164d4604ee2f3e43942"
                            },
                            {
                                "filesize": 4711678,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "b882e1118802034a207da2494a6034b4fa07560d3249e9ad4fdd06f55794ba5e34afe0017a3815058a357cef2b85e41fe9692e6987422758e3fd20f66f52fab0"
                            },
                            {
                                "filesize": 21495032,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "46ee6f038c5760f08fb016c3c74c635d984e39ab77e5a6a9d5b1786631a5a42ac5788f39d1758b0cc132e35114f1b3908bbe79501809ac70a8719172b6625b73"
                            },
                            {
                                "filesize": 29347136,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "ae06423268df8c066037ecc33f99c7d23742943896cc2c1d56cc9cbd51510a977a914434ee5b3300fca49e15d543708fa3757acf2d1da34f8ca6d4d1e2984fdf"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "hr": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53445762,
                                "from": "*",
                                "hashValue": "71f8fe37f59c752d7b56537622fe4be3844a66b517ff83bc75cf80ce47056b3b7ecb25de9c775dc7d64a862314c8eff897eef588a9ffaeb24f7c242488595bdf"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 21502932,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "a43a2f1dd22e96fb2f3624c7ecd1f93c1ef6d90b4c7a5afc31832ea97533ef33a5b6828da0215679f9017f6bfd8f2e0a894f04001192e122c567908bf83eeb90"
                            },
                            {
                                "filesize": 4711695,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "372e7a3022f611542a044161c2c59bd36e1b071271d174cc124c676879af1a826cf68350ce30f8dc0a13cbd83a1a4a99925c4797a17b243097045feca7d17efc"
                            },
                            {
                                "filesize": 27694578,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "d7aa751095c6370e7cc1b45254cda5ee648c079996e71e9852daa26a8bf18d900a0aa3f37e2d9461220bacae05fd980fc05da3d1d47d92a5a496d17679e8b705"
                            },
                            {
                                "filesize": 29385987,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "41482c1161553e5eaa190d07a08eeee6b124f02bf9827bd2fbbed81064f2ab8787a0840cdd86e206c71d6efd9f06e6695c3a6447b27e4589eb4acc179437ca3b"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "hsb": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53435489,
                                "from": "*",
                                "hashValue": "35c15d5d543949c9c9ebdc2176bfdfeddff077b2b90980e68804223598ffcf50a178afa423e63a60e4389c77950f44cf924da1bf5c6cbdd91945acdaed5c45e5"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 4711605,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "ac295ff05f24d3224fb4990aeca66aee064717e5221243d94c865c758d68c7014856c66827c0e4a856a92e61a752f2d08435667c2c90785d96149679727f93f5"
                            },
                            {
                                "filesize": 29371553,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "d94f55d06fadddd546aa6fe983cc0ec94a1e598e012ec2f2251fe1633926eaa61c5858a75c391ff32deb7b476c545cb47ef7ad086c92c3315dcee738067f718b"
                            },
                            {
                                "filesize": 27716024,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "e25d15ea2bcd949801290110e15c7d63e3f35e14478e658e6f92cbf897f55045c5deea08c446fa8198642468e7842d012774d57e50548ec7c393bb02e63edfae"
                            },
                            {
                                "filesize": 21507066,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "bf5075b267b53c8df1f33612c2ec37cfa840461d47e8ef5db61a319e02c232da4d8280ca48c897a3ee2af0880233eccb3d25e22e5c835a958b023cac7c0d46a8"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "hu": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 54045798,
                                "from": "*",
                                "hashValue": "195b480867c699b7f722f142f9cbc863bf7d6bd1b746c792c7dae75338877d17805c3731c745984e99dcfcb80586676dac1a722e1a0b7f5be1190093f1f94b26"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 21500154,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "1be749b7a40f3c71d8a7799a9bb24d9aec1a8af5cad58457de860ba1d2ee15e5e89c9cc0c310b5435144b18a2bf2572a981afe3c31357f61704c1c0395c897e7"
                            },
                            {
                                "filesize": 27688361,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "ed3650eb908d9c1ca8b816f0e8265a210f613aa66e4a6cf56db4f34b5c60d12e2a80faad57fa8d760c41efcaa3e134dde896f78cdb429f955733c655e2e19c25"
                            },
                            {
                                "filesize": 4711736,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "a9823f14789b174fc297032b62f340892ec29083ba4115da9fefaff4ec412b2cd174350a1e891dcc22dd8bfdaf24ed741fc908a23e1ad45bc0c90d9518df09ca"
                            },
                            {
                                "filesize": 29349676,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "fd344dd106442ed3f36cb06d76d78074045704485bd1160ddb953b3a0feea9d856eff7b44b4f6e4bd23e67c914c9d7e000857ef5cc2a1a18b6f114fe39e1f98f"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "hy-AM": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53504400,
                                "from": "*",
                                "hashValue": "272298cccd5e3e89c02a9d35430a71013257fa3bdb2d8ded8f9eee43f4e9c684faac2b3b4ea801686eb8e0bf75d949bae02e0e29d459cfc64fa208e83cc93e7d"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 4711703,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "15d0e2e52ad0070302456cfedefa25c805797551ab11c4345062dc1e05c7b79d83e83117cbee72ea61301d9059682d295c017cb92e8b2e826de6e637cdf59b1e"
                            },
                            {
                                "filesize": 27782675,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "3b014c6b9e3ab21e2b9466b6d9cb0afa47a62506afe37b7f19dd11dd47a5037f2c73393661689a7885072938d09d67e29eb5f520f201ecc07fab811cee3169ad"
                            },
                            {
                                "filesize": 21484552,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "2fffdf27341a80a2d9791d22cc426a938a4caa5f48be1f2ffd3783e2845c1f8b44621f54f80929c9d9120feb0de5848eb0882aa716cb887afa49fc366b8f5b7f"
                            },
                            {
                                "filesize": 29443984,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "7831b09e75016703de34fccfc611b2c5a791c74d6a5acb677ed6eb943aba411908272c35f75e57e3b38bd1313669657cb005e8b3f789f128e26c45e7aa6f07ec"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "id": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53489981,
                                "from": "*",
                                "hashValue": "332a93dbe4a3a35c06aebc760e548e9b079f69cb51351c48cc91a46d9735eaad3bb20eff32be2ee29e15cc04f9e4ff3ef5a66fc005821b643abb259fe85951c7"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 4711672,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "017b9c3b6f5fc91cdbb4e458f97df0f5feb0127565d35307564687da2e1808ea03d8a9f5329ad6948ad81aa9d581acb5a074f6774615f1f66e38bd49821e8080"
                            },
                            {
                                "filesize": 21486272,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "cc6edc57ff0eb375d827670c4ce32ff78e00ea8815a5e1cd156cec69bb7d482031752cf3550e8d41936a9dbe9969e665fa116516091393789974655db220af8e"
                            },
                            {
                                "filesize": 27691889,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "49406503cbf26364bf2e49c2a9ec7e2515f3b7fa99cc0a9bbff1feb28097ad6b4354d9e13056cf086037681a7cd69a28e4509799ba5a0db8406959f936acea32"
                            },
                            {
                                "filesize": 29353957,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "0d107d756d070e3547c74000ce13e0c307e1dac342cb7a8d9ca399aa68d9107f783ff1d64d0daa4b4e4612ddad7f12d242322aff02e8de81fccdcf575bdc0677"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "is": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53452862,
                                "from": "*",
                                "hashValue": "9017505a8c5c0cd950e4256d30f975953189ef83aa3e8f78b4ac7b6c9d4f556d1fcd799a206d2fc0d5b2f27178f737f4edfd6cce6632d7d2542310eddc07026a"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 4711663,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "4e51450197b620eb2c09235236a0ee72450d6082cb5e22f0fb0ffcd6b0081dc9a80c3a72df258c6448bb3dbe051d1f22bf8ae496b221232a46fd982b91e1f375"
                            },
                            {
                                "filesize": 29356429,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "0f40a9844fcfe34fac0ac097d5acfd92c9c03003334857c2fcfd801f9bb593597eaebd80b2687d0bfc2962279705cfa217d96149e98a4ccac8626182ebab5e0f"
                            },
                            {
                                "filesize": 21497347,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "d08222b9b094a33cba8bbbd99c32829a38ed2fe92b39e2cc0bfa8bb7769927fba013cf9d1d7943992ded883dc8a6a8db6a1b385915fc21db170072b8e78e17fb"
                            },
                            {
                                "filesize": 27696215,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "4a91dc4945eeeee080a34b75a519bea994019be05cc78675d5eae1fe372dc0244ae96691c3fbded3dc77e01228bf71a37c21aa211de8d3f9d7025a7eebdb3587"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "it": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53323161,
                                "from": "*",
                                "hashValue": "6d5d87c8e03ba798a7370c4ea8f57d3486f292f8217121cf65b01c356f8fb19c6c46600260e69e1a3d0ba40300c5ffcdb48dcc5f3a32c2034d00cb84480a2fcb"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 4711666,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "11004257653ed77ac0fc97626ca8b0393f151a07e000dbd4b95c89f5f248a5e05dee6e1de8fe1711699c253398594152dd6d5aa8d3705f6881a5a2c0e69a709e"
                            },
                            {
                                "filesize": 21460918,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "2ad21e0aaeaeb099da747661215527a98cb8bf2b5384cf4d7cdc689897e7920775bfb6afea07871f393be5470363325fb4ae1f437534b7c47d0444a6668f3800"
                            },
                            {
                                "filesize": 29286140,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "de90e27721458866d54d9d0eb677c732dd04530f7283dcec96505a5093d6e2bb11d411ad38c51cf857213db61ae78fd3a0a45e7b9c22c49ce2821097d9e3ee98"
                            },
                            {
                                "filesize": 27646216,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "bf1788c1df8581acbf8f32b86ea632629ef20116b011d42e5748bd3c2e1b4b4e5db48c5a60cd0105e11739ad0e74650975f684fafbd992c57e8957b4cd265463"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "ja": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53684362,
                                "from": "*",
                                "hashValue": "bc69ec8eaf0fed79349154f4ca4210cfa9376b4909e51df4b6b57c6e05869d57c2e540db00cfd0d5ba1f63d0983a14dafa4f0dfd3217c269f3bc17186d72209c"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 4711603,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "f937fe26f043d963c7ecc16b71557e34cded7d1ba9c3d28aaf365770243ee791e435ddc395fb715fee547b8d8fe0f36fbfa6ca24afd24af3bceea8b707558a86"
                            },
                            {
                                "filesize": 21512289,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "f24386a219865c57308fe9e1f7d5e85bc1f7c69aeb0586915289c9bf4adb892a2e58d74a04f0faae5b9dc47352fd5feb50788fc226fe45db60f28cd6d4a8ddb8"
                            },
                            {
                                "filesize": 27710721,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "621ca266a2e76259aa8cfff49f443e8e285d469bf8db3de0e8ace130ba0c6c7cc6d6a41d67269e62e4004cd10f427e6b8f1bb11e7116bd610ba3bb7356fb741c"
                            },
                            {
                                "filesize": 29360178,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "c3dcce0fa38f2f36f9f8ab6464987c150c6a57bcc5c0ae3f9b0e53cff7fd97fb03c0822ebaa834ae63006ec0a5f242baeb3ac0d745c63de9bcae8e926c941495"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "kk": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53475381,
                                "from": "*",
                                "hashValue": "c212bd25dbf6f1f9c4ebb6a65b385fd47d3d800a7732f948812b7e66fac896f5bb37f98413653ae1d7ac54c9bd17b1813ad62628ee81e7293d493e33a5669791"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 27782384,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "855702d0623721906078123bf2e8a6c7470157816c1e16932c5b9e259f5fc42051fe8a2ddcfb686d0770a12e84a56f0fbdbc56b5f948db083a594cb2021f8414"
                            },
                            {
                                "filesize": 21582689,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "83652df737435b08ac4c497de7e7e868a8713c479c8c60e5bb1d4beb3ea7d8ef0663fa3c4d56156fe8171fa2e27eb44615cee6ac9acaf75d0ac9b94378f79a4f"
                            },
                            {
                                "filesize": 29426907,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "de5117b5014764ae4cb2d400941844a676e082caed41abf7579d7390946e34d31da0430d0e8fd0d463077cb8aa2d0534597675768b7ea736b4a4433ad9d391ea"
                            },
                            {
                                "filesize": 4711587,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "8d2c265f2211af6bd2cd620732afb713c782b552812a4aebe9a2877d7b6e0e74a7d3b8584acbacba35d30b88fe17cf7111fa0da1f5fdd41140c128f254b41686"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "km": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53775376,
                                "from": "*",
                                "hashValue": "394abf5c25414c6a7be98019fbdd743bf644cdfe548219a6cfbc01b8f359e32f04ffeaec936914efbe59a359d81eec845712a9debbaa21915d7fd8feab5378f2"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 21528004,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "cea920b1e765fa33f598a113a6dc67ecc5d64e69c2ff527faa17bc65de7321428009cbd485dcc47dbd037fd03df6aba87f902609af31bc280b83e5502199a540"
                            },
                            {
                                "filesize": 29486943,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "5b123785e01abcda8c38a6c6fcaad00b4ae7822492fbc8306ad095d0e9f6069b241c9c2577e6e32ca104c2569adacb3cb585ea2e0c3e3a3b20adc0db481ad1b1"
                            },
                            {
                                "filesize": 27778872,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "867934926fef93d8e76f8797094fa76748a14bcfb3d5f6472519e42fd10100ee1cbc8e956786f980acc58b5c2f49d550bf70d8822d726671aa6d91f704540407"
                            },
                            {
                                "filesize": 4711554,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "bc1d7ed1e747abfb8865d6a2d1eb69b5555874df30466cd5ddc2a1d2a50f036ab27773eb7303585af53c999ef4350df9f4d88c355c01f50ba35043aa7b2443af"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "kn": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53507820,
                                "from": "*",
                                "hashValue": "1d84513a293ed13de4c9a2f8fe46271b6fdf2fa70e0bb87c4d2bf82ab756a8ba5da2c382733cadac2e7896cb5f9186260f0b84710d4f56c7082534ca1a7eae32"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 4711523,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "c0077e81f3209c48b0cef5511c831b059782cf12b0f18909af808881a2a1347c64ecc7590d7605402576236f75677b2daf6919e9a007db93c54b8aafa6a8e325"
                            },
                            {
                                "filesize": 21510796,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "b1eed4bd7112bd96479065565732ba027ec2e50ce348abb62510963a3aa0ee66611db2ae6e4bd6e6e50edaa64d15335f839fe1a43534a41276a4701930a73352"
                            },
                            {
                                "filesize": 27742761,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "f8cf06e02a3d92bcf3a7852e4c8fdbae8e90a93c3b9adcd74fc6522acbb2c3c95166fc699cb6921551d8231d22450a64235f10704f612e3ff745923e5e5b485e"
                            },
                            {
                                "filesize": 29402349,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "db5e5afd47da449ef1072a0001a5263c17ca6c627648b0224ed50b3afb4e723a7333b121d18b0a1a88317caf1a2baeffc723ef37e1891153b03adef52573e3b3"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "ko": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53435902,
                                "from": "*",
                                "hashValue": "bba617b7b91cfc558d285250a7d136455f8ab1d41e5a92ee333bacb1b71e7de9a7f1eb4ddad5333a6e5c6ff216c0c88a6507fd99a4f55db539326ef4675adf25"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 21505474,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "999bff3a7900d0ce7591ef9429c7fdcf8201cc1ace993871688dbd3d82469051098d729a0efc9d7906e4359a8c18d0376ec325532ab726717d8b3983ed5f7ba4"
                            },
                            {
                                "filesize": 29491963,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "334da1354a0269dfaec2e440d56d3394006d77832717925e1354d7a126dbdf6daed0e895b4d6b66dfa998a9bac89d76bdda80c47d309368f872ba95f388d735d"
                            },
                            {
                                "filesize": 4711505,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "4783a9820270192d0790880639373ed0a6e0ab180db1cc45325a55d2ee3074342be1397cca1917aba5fc0f834d2a31252c3d5bfa8fe2077773d62a4f2f1c195f"
                            },
                            {
                                "filesize": 27858742,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "ae153933fe27ebf6630a43111d0767e81d37db68f8dd4446865e5977cacbfe98cecff2ea960e06a18e55a7acb2e3d75872208062d846805de9d5f5a4ccb00c4c"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "lij": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53592004,
                                "from": "*",
                                "hashValue": "4ba9807a19cd3a5c18bcdd99e3c5377c21f230a4cacd7b0da904f09dc5fb88639e240ab6de37d44cf5005851f01404a4869576c511aff4cacc5883dc86640a52"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 21713551,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "d9dd6520cfc2c4f100c799c155b17cf5a275531df5647be1d051c855341b9f1a431ff58e49517532ef213b7cf4301f8f097aeee565dab2f027bf406cdaffe937"
                            },
                            {
                                "filesize": 29479028,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "04e60afbf2452ec584f0e6b028597f56aff910c68d9a6fff38d820a2afde38f88eb0aeba5a4eab32793caedf58ea2d1de2036d89c578d5a1550a7ea83cdef82e"
                            },
                            {
                                "filesize": 4711552,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "856065340d69db3518b9782b73cc2035a262e8633bd7c15b7b3b19b775be412aac10e7d623028285e3f54715f57ee3191762e0103142a50cf5c1f1f350b99de6"
                            },
                            {
                                "filesize": 27855666,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "90ba3b88e6da553f2aad7578578c86a1cca6c9bb884bc2c28394df6fb34bc385718bd12009122b2dc0badd18962006807670c04dc062f0460814a0b73b00fe75"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "lt": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53775602,
                                "from": "*",
                                "hashValue": "0b59c9694014ce8b4bd14ffff07d1e1127496bc0fe749aa38fcb9fa5a92a4f031be7fd0bc7af8152cf2e6b71e72581b8cc5c626f0dae8503eece6186ae89e609"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 21545742,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "191531cb03c3fcd8fb83a26073d6fd3498406e2de0b78c0ae7599ede5d383f7204c4968589a03e5385252d7c7a45a098f9776896014f461f12425098e47abdb4"
                            },
                            {
                                "filesize": 29407724,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "9802323582291a5262c493e592945cb0ea8a4aec47a928b27834cbd982dde619af9e975212d5e10ac1a5e43cbdd75c9a923504be9b83ea88db9550b447c8a491"
                            },
                            {
                                "filesize": 27775167,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "57f9254dc2d1ffb4128b37dd6cb32ad0e6c2b77b10b3f895e5331a8376f03dc95ea4d9524fbca961b3cc574ab63c7cb65673d575f925eb9a97763b67d1b71c3f"
                            },
                            {
                                "filesize": 4711534,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "c9d3f64e5c08294e5188d40cc7b4f39afab91a4a008872f125b2118a0d158e7d17908a29dcf8af8368ddf9a055aa53c2cedfc61f0e83b8717eedcdcb1d389d33"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "lv": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53719231,
                                "from": "*",
                                "hashValue": "4b748df818a3cfb7b0d668d0fbcbc7569e2eb680f94190d6a5e7b6235b7a5c9ec101e431648b1d2b1cc0aef5d4859af806a6ab6f2c766193cf4f882a359cee1c"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 21504051,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "05538d1d8e87f03d12ad33d312878ddd736ea5328c964b9100f73f47a39378f7534f893db699fa730e625113bc94a720fad7394a2cf83ac30774280abb7ff882"
                            },
                            {
                                "filesize": 29354830,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "e99e4b23ed349e385d19fc86ec818d4901fa3da4997c262e12b2e964fb6979937e7ab82ce199263606b67ba92df92cd56c7268100de19c2c00821554956ca6dd"
                            },
                            {
                                "filesize": 4711693,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "7dfff59998def35bc2aad4741095cfe76539f7be01d31993b4bb2e85f5c2f3a3c08fd9de8f815c9c2aa6aeb1c6868ab691d908a26953bd43656ee812b0d3ffc2"
                            },
                            {
                                "filesize": 27695975,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "baf65fbe54131274b954b3bfcbd3db646853a89f7001a2385f1f5d195a1c3454a684b2fb22afa4fdddb05495c5e7291aeb4507ce295b4cb28a243b36c6ea805d"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "mai": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53484770,
                                "from": "*",
                                "hashValue": "fd9078ec788e474538c3ce51c64189a7cb718be1d6ef6bcbd54b68737128e11e58752d4127ad1bb331a03e5d387e619aecd973e2a01db07d6b530c1563bff7ba"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 4711676,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "5963b80ce9bab03bbae491b1d72470dc96b0c2aff9aa865c6de3dc8bca74d7ed22375a7ce1247a0079d067e45fe8430fa56cee8539dc118b5d72d3efd7cebeb2"
                            },
                            {
                                "filesize": 27683881,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "36308cef3b9d45866598990a9376e27f51d6497217586fc36e7d22732f06772c51e5eb87e1793fce6c2fd6db82e2c341d72668c772731bd3e4ae5f7131e09585"
                            },
                            {
                                "filesize": 29347949,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "38d3a2c72c63c1aea56092ab15b7ed0ad6b15b24f2b90cecd098dcb8e73a963e76c0f4791bc3665848c834178f07698460691ff3e732295a802920df880dff61"
                            },
                            {
                                "filesize": 21501527,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "cf5c3863f21fcf062f6a9368b3fc6bf9674a5be92d501bf21ee0d2f561a7485fd2ce6e7840ad7adbb2c5e2d7a88ba379202f6bbf90a136660bd6a1d4cb327d8e"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "mk": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 54221312,
                                "from": "*",
                                "hashValue": "3370f9d4b107a370b5b6faa54e09cdf044845ba1bda759faf40f37066d7842f03be0b11898929a0a0327390485a3104ad7ab7a69a816149be53c0eca0e5912da"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 21504553,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "cbeb2442ebe1edce6ed1b45033a7c6e2b29b84ea77b4f40ae777c500bb6f478710fb64a9603d2426e4c64048a2b8be4e418b4ae3fcbfd7e7aa21f8247baccdae"
                            },
                            {
                                "filesize": 29364991,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "8ac546d20fc3fd13f9398d6528f99acf1726e35a338b781e1eca033efb61b81a3af0a21325b24feae913525be674d1ff1cd4ad5dc6a1b45ed90b5b2c960311e8"
                            },
                            {
                                "filesize": 27699683,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "cd6394096c2e47dd6760c3dfa073d75a1a851ebc872c7a579c8df64d74242e3cde00879cd30aca3cad3e434f1158f5172464cd2ae6661b366c50a8f60a1139c4"
                            },
                            {
                                "filesize": 4711708,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "861ac417429a57a5146dc43cd6f3c891dfb9516c347af94895574e753d96e952c9619ff59f367fef7dfd68c18eecdaf248b226bbf6e3aeee6029767a286a7c6c"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "ml": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53497621,
                                "from": "*",
                                "hashValue": "748a9af63a6989223ec7e416d69b1fb9ade9b5cf6c55f2ee121950f3cda0b07250689c8d894701fcf5979cccb6c11204570bfeafc6fb3eb62ad84b6bcad7600d"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 27856096,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "5ef6019ba19c3e30fdd71f610b49d6e05eb98c303e0874fba2cbc42e5ac36f4a852b5d9897d7039cbe6b43fab9a0cc87fbd9f46bf8d45f371bce8ac2bd426e2f"
                            },
                            {
                                "filesize": 4711647,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "6a2836e9e5cc38d422dbb2054cee88271203563d5fcdf6eeaca96e37cbad66784d4a5db784d9a735d8739d59c712c01d6d8afb968d4ae7a2fb2701f993674529"
                            },
                            {
                                "filesize": 29480152,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "16b8113c74e32163db7d14d7c6211f7be5f69f8080f323d6d0ccf96acd7e7db35b33b3228375863bd80c0c33ce4f981eeeb0b19eabd65acda1b450d984341538"
                            },
                            {
                                "filesize": 21505349,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "cbc3de25996646be4c8f4474206f7c454e0deef37345d5df394382e8620f01195578fa24a104e8ab6f87a38be0c0bc166945bbbdffa566be5e53e644d99ed906"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "mr": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53485718,
                                "from": "*",
                                "hashValue": "16b562bc354c8f7324f5f13adb1bb8723a2a77a4c361b7fb99e4547a9938efdb57f7c4c2c0dfb9bade87e4fc99920554a8fc17e9651c5ac96d603d2d9e8c8914"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 27846631,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "a8df12011fcb16fe509e2b54f55a687b5657d712dc68c343be39c033ce5c1cb56300300e536a651c1381ad8c0f54ad5b32145e70743e98c54835072d085f33a7"
                            },
                            {
                                "filesize": 21508927,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "da16eaaff45554ef86c22de23fa05451d8ae207b20e88bae1cabd9e73b15d64f0e7962ae191b7fc40d35a3f93339dfe171ceadd7734eafb1c1df3502fa473caf"
                            },
                            {
                                "filesize": 29472738,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "1147775a677701f5ab2e8de4912b287e15b8335a4678465884d0200f225cb471990b0470dd8490a0ca186190ae12cfb865347665f46a0f32700c1c11894405ce"
                            },
                            {
                                "filesize": 4711657,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "47a81eda0f53799d6f6071d13b1262adfe16ef217bde19ec87791e303845c61ec3504885a83bf024ac42e17fb0e0324fa35066de7d06d23e12d6f95efbb97f36"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "ms": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53458736,
                                "from": "*",
                                "hashValue": "fd83dd4aaa6ee5782c8731b9e2e0b22d5d8e3b42d06cb2a5c9412545af68b5bffd35bf6258fcd02e3f6b0bbabd701f7bb967419a55bdfae66c84823f1069a9a1"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 29423998,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "641875b9f4495f14fc03792c975a58877b4a2f48a1756bf557e828dca8689ee56493b26c87978107e739ae78b80f408d6ea3f15f8228249614dcf96895a835f7"
                            },
                            {
                                "filesize": 27788274,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "9cf82f4dff091256c61c9c4f7604e2236d918f2f0fca40792bdad3cb525c63c2d653dc85023d0b32978b96ebfac931e79c8bd624ac9412c5b38b52c1d1141c6b"
                            },
                            {
                                "filesize": 4711672,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "121a783b9190469249b66ead61ff88041651710e0d3006cf9b46bb6b5556ef4e30c4e1d1f31382375f1cee784fac172236ae08ef3ba1b1f24a222a1852aa2b90"
                            },
                            {
                                "filesize": 21477620,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "ac98db56a95f5f0174e608655e8b20c5fed97b1da60913723f5b94eec23c8c39a862fb7bed1fe62cfdd77a7cc1aa802122ec37e71c41e77cd55e7c4a86c0369a"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "nb-NO": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53409239,
                                "from": "*",
                                "hashValue": "8504be81dfad9b0915c412e77a48c7a8731e868c8366cebad5496d116b24f931eec9c031afe5e997524d33dad087aa5c8a2a1d5236a3aad462a2d3e3c7950106"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 4711665,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "7c5c03056239f579c69fef241a509b19d69c954eb01357e5d4b2fc867adc97fd335398e45a83ad406a2fea1fbbfaea885e06e234af9b9d901ddbcc2b3a5f1965"
                            },
                            {
                                "filesize": 27675887,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "54f11d82dedb858103c772f74b88591934bb9106bf6ad9f2f64cde506328b24563f9d657d1987858a3813121833b8717f8c7ddc70fcf9206104e9aa72b447a06"
                            },
                            {
                                "filesize": 21493015,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "ea24e78474fe710eea5b7ff9441a1e031838c592cbd892bcf8f83d20c2d4ff182e8a6327274606ccbbd9114ca9dd414d9768ee89a16690190848f6aff2b5340d"
                            },
                            {
                                "filesize": 29334720,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "af92fe12b22549b6d90fe080a9b0615754d1e0e0826d54d7a24e5081b994a15404c64c604d79d6dda822c0d275fac45b600a1a1d9f1808598004df12c60f64d5"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "nl": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 54172571,
                                "from": "*",
                                "hashValue": "8f32a5c6469f5e7cbe6f3ea53d64cf59e75df65804aecd7c5663714b4e3228d2af3db24113c68772a3623682a6742f20d258722ad5f38107c9beac4b3bc1d4e2"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 29346656,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "7ecc311acd577c329fbe9cc838b25c8b2016e92fe4622fd5a5ac84ec802219f13c18ea95f189ddf0e653379a013f02015029607cc27dde50a8172dc94d809036"
                            },
                            {
                                "filesize": 4711672,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "c6ac68bf5dbc0cb8b7e794f94122ee5a201335909ecd1b7e88efe7734786831f32c36fdd1a3c9112699eefac4efae29a398d2e040b92a4eda4420a22facc4002"
                            },
                            {
                                "filesize": 27689844,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "02bdcf31a05418d2c1c425082d546e7ae7999e8e9ea21f684f1e37468e6c291d4a84e6734b226df161c4097cd104e9bd202ffc3f5d78f9e2056ef126e2594dfb"
                            },
                            {
                                "filesize": 21506545,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "de6d2a52e410331c68142aa1779c04a9be260040a14bc5ebd46c72b0a9075b38aeb2f7a00d7d31ca20faff810d3ff181046e6fe5c3b8f2fa496aacfb7d9d6bb3"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "nn-NO": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53403718,
                                "from": "*",
                                "hashValue": "6188e909089764ac792cf6cec86477c6bfbabf394d639451ba4e927b79ee4bcc1fe4789c1e0975a4cfd8ce6085441c9d1b2258b29f1226c03f5c5cf2ddf21f92"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 21493270,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "1e39fbe25d03c7496d71c73f75d4c15842c12465ff84d608faf4e33f45b4550e64410550f7b15d5d70c7d87c2e4180e7add00373ba13efdec25ce16e3837fe7b"
                            },
                            {
                                "filesize": 29345809,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "c59f1cd272c2a45b8d10ddc4efb466e4aa224f9a4aef26f108c081c0145b710189b90aeb6cff96d4d32b92f36efa8df0c161dcfce3c599220ce709b53a8042cf"
                            },
                            {
                                "filesize": 27721290,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "3dc70ef64e1fc74fb34522b9698f2e08b062c1c541f65a601f5092f3b6068a212c574007d39f88f6b698e739d6fccccab3caa5b99e42348e73798292f2044e8b"
                            },
                            {
                                "filesize": 4711596,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "b63688e5b0e4a3201b5ab6fc166991ec7e515198cb4de50c4c76e0d39ea63f8c55edf84d24e57b8493fe2fcd5d283b7fcb0793096a081f4c48068f4ee1d5a1e8"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "or": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53724841,
                                "from": "*",
                                "hashValue": "95f637e35d358992c2b055becc0c91cd7b1a43761b36cf364eb3547cef514572d01e4704c8a44f7cf5e6061e7b88e03e4bf7a2b79e91ad62b181de04341d0623"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 4711721,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "0c597fe2a18a0508641813e16d7746166349436c84e0f8526cd400720d2126f6c70efed3e958285115897fffb6924df05d84dc46e2121fccfce0ea7165da698f"
                            },
                            {
                                "filesize": 29359390,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "cb6f6d6cc652161fc0eda14211562705c32f89128b49c02e9aee7939929609a6a357766fccafb272d2e47eda77fbd90cd0f15c5b7d061f243258ff8d8867b094"
                            },
                            {
                                "filesize": 21506669,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "690bc347fb6f6e7dd5ae872b4edfad7ae8a82e67721eceb1f00e3aea29693afbd86097312db950900feacbf7c199e8c48088e9fc6c9725de341a8ab7620930d4"
                            },
                            {
                                "filesize": 27697497,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "fdcd552fda4d1a1e54da1e0edbbc59165883dceeb16bd25186860a8bd5fbd8ec906dc33205358d59c1796c95f83b0fedbd152b010fa1683a338cfde6f63b7825"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "pa-IN": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53466801,
                                "from": "*",
                                "hashValue": "90d5c95e33552d3b6d3035dcba4bc6452794d9d112e4b545653239ffbd48f5bafd2a52b761b6c58d31d3159d4e7f1faf00e19572bbc6b596fb0f4bba76c22ec9"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 27683410,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "60ae8ba703bc3d7d1c4ad0c1184ad2cba72c12729c0cb466e54499c6cd1c516325c6d24676eae02c36193feb25753cd9cb1b5f10562e0c0c8afa7ebcf1ad6cb7"
                            },
                            {
                                "filesize": 4711703,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "716e790d7fef277b07518c0202beb9b45468ef45a8742ccb2b7615b7354fe2e60e29a80940896956d0680886fe2b366e42558e1817a3c5456e3fb1930109f7a9"
                            },
                            {
                                "filesize": 21500591,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "4158d37a4dd970d76aa608a31de83e6106799334a4dc0b1bfed1f01cc0bcdc060a61e197d41d828210cd16e81d53ef979d77c5034c5372a609cbb4a34247031e"
                            },
                            {
                                "filesize": 29341898,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "8e5e53b7aae0ee8ea4820551b42c2029dbb7fc3bb4c6539cc7dafd2b072868afea6afdad5db3acc3e43f7772bb737e38a4e26f4151d12078250f99089d7faeb9"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "pl": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 54483553,
                                "from": "*",
                                "hashValue": "ac0721fb844cf5750048fbfd86156175be091af1b4d2bf93858432d4e1a52e82572d7a26b7fe00c977bf8716ff98c46c2519e98cd6aa9c12749e48907a25c00c"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 27659166,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "cc50dc6d7196b5a34a0ea815c32215879856bedbe875214da900e505b09ccc9762a5de890c37b758a5fbabdfa474138be9b62a82270ae9a3768eb859d757937f"
                            },
                            {
                                "filesize": 4711719,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "afde37a790dc313897d615ba9f73083a281e616e57e68bfcb4c5251170f9988db51dea8aed7d2c1164a0bdd70a79580b194c17c8aa222e3947800b1e78ceef99"
                            },
                            {
                                "filesize": 21470423,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "bd7a376b482f047eaf03bc078618428e3be311ca01c0314b94c6a1a0ac53a1913c93efdf621560c2042d0ec401dfaa413064a9f074519b1edfde52ad2d69330e"
                            },
                            {
                                "filesize": 29308708,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "9bda24c3f9245c458ac888e7fd5f0ec6b0165804ec0bbaf33bc1a0236381fbf947dd61a00608fab60c4acdb3897e39086d73c957d845a15cbd491992a0b7e61d"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "pt-BR": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53604746,
                                "from": "*",
                                "hashValue": "8c353d18bf9ec9f98ae4fef1cdad74c47f0e5b1738e5f353af05ef0d5101402a0baa4053d9ce2d73cd284b125f029f3ebf3c845df9fc6059e4e32417dc01c1b5"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 29417570,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "c9042bd6056d1990d17d79ca485ede3789776740e9d4cb6ce346787649c19882025f76ba9a6ad58c965616e008f60579a8108f20185fc9272e53bffdfc5a1e9d"
                            },
                            {
                                "filesize": 4711763,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "ef7475ffd6f25400d87bdf35e2af6fc7ac51da55540f0bfd52968a178f8b7718956afa7b61801aee6c331a82bc785ef7fec0d98a2b3ccf2eb5559650ab575d22"
                            },
                            {
                                "filesize": 27701904,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "504b5f821c8f8e6eda57e95e460f9017939a843207bc0cc1e1b86356018bfd1a882fab780b67cb03afb3903f73a321412f66205cd955cfcc2e25f4fd9a0336ed"
                            },
                            {
                                "filesize": 21487849,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "f405138039e51612e9a6c53c4c014e1202322559a2186e244b1b9e35d06251468f335cbe93614364fa301151e66fcc3f834747505722551f9ef3acecadb8d223"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "pt-PT": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53595318,
                                "from": "*",
                                "hashValue": "0f6c36482170c5651d34692dbb32c8b0312d94cca0228254f7e0f5093dfb252085fc48a73f5b8284f317d553ceac9665a8395782cc657e0fcb90de8822d2c06f"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 29462067,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "78b828ae09007aa37117d7e3fae5f974cb6b61b54734b0521229b30fcbf99293e8561461460949f0dd2384a5261d4774a7dcd26a005154647529ad7c282718e0"
                            },
                            {
                                "filesize": 4711748,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "ebf1203fddeb7439fc693e0b1862bed79add4db38c15a3a1373ff738c716b61d511525cca975a6ff1ede3ed4e91fd234338d8fa4a2b8a474df6085f549213826"
                            },
                            {
                                "filesize": 21577949,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "caf0c9cac21078c4678dd0767ce8dfd5adf514abc731661300a58c8f6a71c97068c287b40e0a758ac783366e15d30ebeaaf8403ad7b203935abb4a293de03766"
                            },
                            {
                                "filesize": 27785516,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "59ecd4d7c0526a0c01a27b17440093346605eb41b86b80230e4f6bc5e5b3dcea64153d124ac023bd69bbb4f47c779a108bb2f36946bc6e434e4638e231338056"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "rm": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53414242,
                                "from": "*",
                                "hashValue": "b9f6b261963cf8323206192095d8ac70339426aced4c138b0f78f0656d5d3c9a2654a6d0f60efc3acc48dcf9c7cf6330d4e3dd64de29c0ed6178dcc9139af4de"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 21490189,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "30560a05da119d863afcf7dc78c3389a67e6ec49de430800a178d11c64287f5a519693d19ad91b1fd707c93d8a0fae78189e63697e5fcc201036c93e0f99fcea"
                            },
                            {
                                "filesize": 4711716,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "5fccb9ac4db1e47c49d3180451b8c814606d93be7a3de1a31509730dcbe182a62eab8da99e9b5e4649f508d37871208311a353348c90c346d333c1d16f280b50"
                            },
                            {
                                "filesize": 29410885,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "21b0b8dd935997da98cc47a7e64afcf4f649fdd07c3f0b6ea43498546c2a7de8cd33d6884a70c125e1b663f69a034d2fe9d6b15be5dd99dde0dc880c62b61982"
                            },
                            {
                                "filesize": 27785625,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "483c2a2d1c8bfa1e29901fe2521e4e645799222e776280558e371d10e93b9e1d45c67fcdc8916a5d1bde296923e03b9881fb75f8b8444233c9aedb25b7e7462d"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "ro": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 54098277,
                                "from": "*",
                                "hashValue": "e6604853a38bdd058716c37839e95d830217395bd5254893a0526efbebeb13381a3e45a49921b09b22726fba9691437ed89e321e435a36da03b9b33d676e2536"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 27845583,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "31a794feaeac56ee96143b2ff1a2d461bcd1c98c44593395af9bff0f12997ceb1518bee194b7d099d1a0e8c9dbaa6df306db0d2da3e4beeda8d92c453942dc32"
                            },
                            {
                                "filesize": 21515961,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "6ce105a9e2b44612b0000c0e4f506bfbf33f8b0c24b317f9ef1ea5cc63099200e31e7c9453eaec39a196732774083b12aae0de6c6a9adba6fcd179dd2f2e3d4f"
                            },
                            {
                                "filesize": 29484456,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "2feb842a3e24d727853be4160abb2db3a4421db3982d9165357279699bc8d60cc77bf49fbc575f3b7e2a8d468a1cb3083d9e6568311cd038dbfe6e6fa495e561"
                            },
                            {
                                "filesize": 4711762,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "3ad8aa1b596953459d24b02b1a30337e786aa5d4a1726738d765ff5ed935e2e2ae20694dcad053f98f7e33e7c5b162e62e6a3d1fa6345fd0fadab570d8cc203c"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "ru": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53898409,
                                "from": "*",
                                "hashValue": "58b7bb2f6e38b1600fee01973b2f82eabc878ec2d8b946ccf3921ae5e4530c5dd470263597ed38dac1684e33447a73ad60c72896547d6720ac6b36474a3c0d84"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 4711728,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "acce2db6eae51576ed9ca7af992d562fa741605f411d9beb905041912e8836deefcdc632745dad2d0b08cdcdac702aaaa67ecf38b6696ad51543ba12e4cb4556"
                            },
                            {
                                "filesize": 21473721,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "6c6020e990d868ba835c21ae8903b76f8740cfe6bf7d1273dbf6cc2ccdbd0d73c981160e38ccdeca6b5ce729c118067a19e1674201ffe5af24da359542ca9150"
                            },
                            {
                                "filesize": 27658347,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "81675d4d218d5c0697ca81010cc6c98be92d2eb2fe1d31de9f95604187ec043261d2f789eb3fca33264c8e44a87e3a345161bac774d5435a1bf28d01509ff1e7"
                            },
                            {
                                "filesize": 29306809,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "02fd90e646b0f5400125b5aa0d8fb0963c91e8215df8771c6a9ec3509221a76ad21c871aa45dc4598307ecf13cfa6a5377d77bf724156dae5c400c2a0ccf33e6"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "si": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53506161,
                                "from": "*",
                                "hashValue": "2794d83d806335fa12d6ad1fdf0d4689cca56f9303e63555bc00646364a7e1a114ce05fb029ec874267f1c67276166e283fe126f4d30d95073e5046fc14ed478"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 27855143,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "871fa1982dae103d1b0e5f69a06b78d18020ad8d601365a9c37c67c960dd261b2d5f1a8a664fc64c47a81b1285c066116b8529020632cf5947529fbb32dbc484"
                            },
                            {
                                "filesize": 4711649,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "c641fce41dfd6480e14aad5ac812c7531fdad136e1814cbc80fb6f7459fef5497c158ec1ff154f1a857144218e6b8d774890ea250c7d1cc8a6a7262e60211d81"
                            },
                            {
                                "filesize": 29491196,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "29c3ef1103ebbb9c28e0a096072dca6e7ca5fe2bb16b245840af7dd8eaf4512aa3eda844d03609533e7cddfa24b11f24ed328d17e59e08a4b5a80fa3c241f777"
                            },
                            {
                                "filesize": 21509338,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "3877a278eea7a9be696754be112e37cf22fd7a4ee09af5a55a20e3ce8b616c6bd5471abc31e5d2431682801b63725a89ed0a9ee4158aa4ec21996f973c9be585"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "sk": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 54337343,
                                "from": "*",
                                "hashValue": "517f94bf8b99595bc68bbf2eb97926d381a4cb66139f8ff15659178bfb8bcfb814c2ce0325905a1cb1cac13f2a4028554274ee5a0122432fd91f0ac7389bc7dd"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 29345420,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "654ecf5eec31fe67e0a830d62ad9ff4e648811855e4ff9949d7276ef2272837aec8163ab793706fd327599a10cb728e2f7e410ff6ed3fd4d3f34e825ccab1138"
                            },
                            {
                                "filesize": 4711728,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "0d778a21170ada310b6d7a8de21cc88f57fa4b3e7317b54cdb47b6ea394f8bd6d21051180d4a30324a5870e6e67e596a666f29767e8e754359617ad88f2d6add"
                            },
                            {
                                "filesize": 27682139,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "04e09c3893daf541c9d028ab1aa189957df23bc491c271b999422be99b6d9795a789bd4d8220a31838c4f2d92ff6e2192e2f4d8b78392a48a5df023e5f13e8eb"
                            },
                            {
                                "filesize": 21506597,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "5f64161ea7758efce0f764bff1b734bdf49f10c00186eb9f57909bdf8bd52bb73035ee828cb4fba6977435222bbe35139fe3a0f12c577053a40664a940005049"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "sl": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53410385,
                                "from": "*",
                                "hashValue": "37e07095c600abf3e9576077404f4627a82093efdb3d7ef922479de5919bce5f7593bec033906ba35b758a2202f9495c4415a6b64c752e8d946bf33c1011dad1"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 27689108,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "c8d1b234ee75acbccc314cfc484e9894b392ac6cbdc099b66b9b6c43dd922d11b8aec5a30c40406ae43cfdf8d55f09d50002e752c7fb779ca15f89b4b23650e6"
                            },
                            {
                                "filesize": 21496860,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "99a61e84c00c2f8cd23e6823f442663bef8ec98e9c76335283284b7fa26b4629998c3c013785b21c4d07e77f2f6620a86041a6c6201bce8523ab974d2d5ea740"
                            },
                            {
                                "filesize": 29345863,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "aa6c6b23449b886fcbb286bade9d7d4ca0fa21ab2a20ed956ae6c2e0aaebf1d3c57f80de3f161d04017d6027fae8f21fcc9fc1deda7cb88c659c1653eb037cb7"
                            },
                            {
                                "filesize": 4711707,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "e4f3e192a86d2c9b07417d5278b02b70ad0038fc8de7c774b56f2c940cb0055471f8013ca34e90a744422d1b9525182920212d6b5089cac15e42c784ecea6d7a"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "son": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53416573,
                                "from": "*",
                                "hashValue": "c7b4eed7d8c6c29d207662af5f072fc7a34e80b03c2343dfa5def278204fc96cbe5cbe83ec2728925740719ca2cffbaabbd70f264a97c347476c09e8feec48d4"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 4711571,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "228da578e4093469f332e4ffaf437e29504745b204cf0c0003a3ffce0d746e30d6bb2cc3d8c4eaa8d0370c5f7ad5794b50a57b97117485af1e222cfb2140756b"
                            },
                            {
                                "filesize": 21490124,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "17c187e9b8903f69645371f5e79d521343085f0fcca8b7668022fa5717d2f3739e08f9af6e3d7f1d813fd89c0a2e0a8ea650d44468951d977ed1a17486be7e8f"
                            },
                            {
                                "filesize": 29381056,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "115aa63c024648b3bec24dd9e8036137aada09e6e171c68ba3f8fd90dab2a5bda16246a7787c589a410b09469751dfd8dd36308d3395f530604081d0554070be"
                            },
                            {
                                "filesize": 27729888,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "9befc0421ade9c30bcad505b7c5c32abff40e9f2a3fcb04a7d8115bd8a1239e60f58dc815ed001493a8c9a498229a9da866aee5b48c8fd00cece35a14c2c56d0"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "sq": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53453835,
                                "from": "*",
                                "hashValue": "298c964e05a7b3c7b60bb46f0fc4b0f1eef20a1bdd201a00579596bdd95dce24776693cd17297c217b4d4e725d7839c8792daf9ced3b642ac9f2c5d1aafe60e3"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 29382006,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "a5c26b8a3aeb1ec76e3c1d4416e715d361925be737842321f911af079c0340637862661b68bcdfdd9c285da25daf0b4067c8604d6f80701b3cb4d4c3a59c9f27"
                            },
                            {
                                "filesize": 27747849,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "4c69f26ab4a37aea3ee02774bf2ff36b1fe484f5fb616d5e6ff68bb8e5d5a7d146a4c5990906ce0cbf35b1db799d311ce31a92195533d0d1742fec8a9cdb7c94"
                            },
                            {
                                "filesize": 4711585,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "8861935b26c758ea21bf283cbbd64f39686e3229ba4634055c12d59900fbf17265e29aa4e5a74fbc1f1b0aa063580c9baf6864b1a8ed5e9b69a2fd8c8758b8c5"
                            },
                            {
                                "filesize": 21509471,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "d67cbd710654539142ab4218a38f989b08c2b16652297e09b2ea0f30d594bf6d23b41d05a9601a8e28a33784452e13dd38f1309b264e98543d726fc842117c3b"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "sr": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 55348549,
                                "from": "*",
                                "hashValue": "aa7b6db141f9deadacdc00682090cf8c6b7617de80046943bbcca93d15324f03440be960c6c58884e742c30c6c3d7830ab85a7c9ad5da09396215c5d9d64ea0b"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 27803713,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "80f305950613f15fffe3f5c7505f82cef9bca2e2b6833336f2297da31e0799f6f6b41b4e8f441e9ff20fb5b776f92abbb4dd2b462e86667955381feefb18989d"
                            },
                            {
                                "filesize": 4711697,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "3d53ef1c25fb3919aea54f1dd0ecee6107143568138b80705dde474d79dedab1f15d3dae55f60081c0adfd136293aadade375b65a2edc0900db254ac9746b4b7"
                            },
                            {
                                "filesize": 21500360,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "5b3083a7ff13692bf4cfb975139b23a86537358c11e577bc8556b762944badb0ba32e012d98f01392057c1ff452148772e375d978e4722edcc696d70cdfbf626"
                            },
                            {
                                "filesize": 29450762,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "fefcf13f6bd9353acd64bb4a97ecd522c30b5c2d91b7876047cf6725115bf0cf61cb031f7b3e72962b522eb9721af5a69f5aacb1eab511922a75aea2d48e7948"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "sv-SE": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 54045095,
                                "from": "*",
                                "hashValue": "3d48066231a746ce17c052202c400516bd6786310e3372fc8026ae0a4fd4f7d4695ae542c0ffc9b88e8245f3d342c3e5ccedbbbd679149916c1d5a445e9385b8"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 27697969,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "d1258cd4834326f49322683af0be01b5930498b19af5f38d65685a74e5782588075eafdd29b6f4b02da37ec53fe23a3e870480206814e8de535f4362ee230555"
                            },
                            {
                                "filesize": 4711554,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "763e3e6c543ede0db90c9044f6a71e9feaa92bc3be7321220d1dcf5178efa0e1cbf4eb972eee09044b14f2033e323e1cb0bbd73217d8af30451b863b9c8ab963"
                            },
                            {
                                "filesize": 21486850,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "c0d93163c8187d78304aeddbd68dfb3465b13c08e0e4bd53a7acf3e3641f625c39211f9b5ec2a78c03ce1afca26f54d0870a25e8e0d64fdf0103469699e118ff"
                            },
                            {
                                "filesize": 29352131,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "53f04ae1c76b9b2178e8f82e6c22579daf454c7007808600a1faee9c5d2ff0c8b3dff2ee9ff249f5b026ca38a27ecde32851895618a1f85fd9e782dbdaf71a47"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "ta": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53732078,
                                "from": "*",
                                "hashValue": "ef635a3061b326bb5ae9a45aa6479590aaea0b4ef8a753166cb955bff2a1140a4c09ac67fdcd37a3ee5d3eb5db4e5fbe0c9173f856e1114f9bca4d80ef88d2c3"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 21498782,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "7c517a4adafc360cb61ae600881c510497ca8397c4b9a81ce417b66800e477e596b13846d587c18c00b31bce84c16fc3075bae808f68b84480eeb087d9728f37"
                            },
                            {
                                "filesize": 27685753,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "d856dfb49c85ea55f51b35c9636846ad4eee6db0b2156324fb9e759b277ba96f124660f6b54c5f33fd179f6f6dbe54bed7c101fb1b697a2d3ee4fd25b712235d"
                            },
                            {
                                "filesize": 4711638,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "42a15c56319f12bfc1f44932e66043ad5c6e391ebcd13f2ebd6219832722aa921d8f02e1c2d16c0e3b455369ffb286410847f42e7d7844e5fd406c6bac8dce2c"
                            },
                            {
                                "filesize": 29362366,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "2ff10273d628b68e43bfe19e74310d5bd68833ca404c1755909f98477eac85006b1273e90f37c1413179dea07b078f8541ccbeef6158780525627159dacbe6c1"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "te": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53495839,
                                "from": "*",
                                "hashValue": "ba1390912bd21602d4773814b52f36c86fbcac4e8f18f26e8ae9ba903b46c7c167f57e1b189db5b5b161ca21ce232e4914eb5e231c1861410ad8e51d3ce077de"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 27803019,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "3edacde6439a14c141be6c3a4cf1204293b4aee9f14da0e0366335ee4b3317aaa71688c49782f9754dcba33fa2ca471fd2dc4e9809d42d48e77d26e4ffb69c2b"
                            },
                            {
                                "filesize": 21485896,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "0feb39b4cea1e7b99462db6351980ffbaa14c930597f420267488b602d7644d03409702963204df09f5ea56ca8a5a99a3210eb8857a3c20a4617e17fb7ec68eb"
                            },
                            {
                                "filesize": 29429794,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "12b02eb23c23df4ed58ac88e1cdf99318189983f88a0401d619ceeba43248f1211154f3981b38b672aa22bff732309995456221448d9e4fd0e648560ce73d79f"
                            },
                            {
                                "filesize": 4711557,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "83f74a550ad90b08c264b1c14757c3ebb761c138e12766b1ad60e20c07057b69533d0dddfef134a73011acf2077181697c24c20e39f1fbfce52f3b92b9081a62"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "th": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53504482,
                                "from": "*",
                                "hashValue": "e0c16ea80b7a6999edd061f20fc12608d22433445d4b1b3d15cc63ac4815d6cf27b1e4472034c83e8eb3b37288963118ecd11a773aefc469e88e6a8d8ad3a107"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 21500028,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "72993e74c46f986717bcdf52072a172fc8393ee901d3790a62ee4b3742cac0476baf774fd06d54abd83ce58cc9186c52c0823c2618e56ff42b7d3eab02f872cf"
                            },
                            {
                                "filesize": 29428351,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "fb16d6c7729287ec5d8579f43379c18ab681c1f365ca12482e8a210743763a71b6ffefbd6ea7255a7b72470d68092f17a8fa5f13a54b68948505b081a0a6de9b"
                            },
                            {
                                "filesize": 4711639,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "1c66d6de0a749d6d62d93f210f9695591faeb190f84971db73adecec2f9d9bfd827ae16a6403ae327ee041b0452cbda269d886cd4fd91e5c7a9341333d3a830b"
                            },
                            {
                                "filesize": 27794226,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "436371949ba0817ff760003183991d488905646436fe9918b32b5a1edf648ae1d0bab0cd6ab74640d4d761f67357d4fffaad2e7bed4ef331cc6998bfa9b70598"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "tr": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53448742,
                                "from": "*",
                                "hashValue": "e08b7f63afc41f413b1ac0885a267f89aef24481644b2b41539ca8c79abc912a8fc707577ec5be42fe33463d097c553c7fb9bc8cdfb28d34b12b2e58cb9b7e24"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 27739451,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "a0f2e1746797de1507f581191d1f8485e4780c08ed1695ccf0cd0e9c4236d55619d1f1dec8ae1272c30c4c709667dac3aa909d24166723476eeb95a1abbb2286"
                            },
                            {
                                "filesize": 21525474,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "102294e6cacecbb1222f13992ec3795a5d140dc8241408c329e9fe9cbf6ef9493eedd688c411deb2127e711e1a39b5242ed1bcf181c77c4ee4157ef627c81605"
                            },
                            {
                                "filesize": 4711674,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "9c526d43f55243dd17943cf0a29c9806e0f73d131642d8932563df4d0975961d2b2efa37131457a13cbcb62d738a9aaac464c1dbe0a441193afddabcff0bd4ed"
                            },
                            {
                                "filesize": 29394437,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "11459fb05e313c6c56d72aa5897c9964ddc3c52275decef976291953f20a0620d6bef30550d1bd3a4c12a30f7b78b2d3a08b792d58c9434439874169a5096d48"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "uk": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53895074,
                                "from": "*",
                                "hashValue": "434953c2f5e2345121623383e370c49e09b694337f812ecf28a08de4c9e7774170f5537fd8f1b16faa5bb454407a49ca4c09432def10ee91f0b6e6a8f32f6aa6"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 29401515,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "b154f4f635597790908afa78547b2608f6dbb5b555ba8d92d04dbfa5c289a5df08f897cb8db542bd1a0aaf12394c0081c64f246be90aa69731f2670c38eee024"
                            },
                            {
                                "filesize": 27726325,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "c67f8928ace4c57d718f9cb6fe1c010abe6f479bddc457b1527a7370c3a9e46b83b86fc1c0c92617a15fcc5a383caa9ad8a0ed7aad5c186acda772203c04fcd1"
                            },
                            {
                                "filesize": 4711490,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "6a788240d206875e92f64e26106ae69aabfc5a9d0b71d04826ef525ebb9243f02cf1644785cccd08916e080e946655655b02b19123692a092c2190de1baca2ad"
                            },
                            {
                                "filesize": 21529559,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "23fe9d34a0160e3a896cc5ce787e76597e49ce165f8beec6a8c69e4c1cf808a7602eb1c6bac472dd768a6478309537d42942e373bc67891621bf5c8d96c0009f"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "uz": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53467563,
                                "from": "*",
                                "hashValue": "adc7e966be603e9ee6fc203e2707585c70ea98db2a4a9a69d201daec22807be1480d151d2fd1fc50bf55ccc315824df56799e6ae2004f3a26766f83e0a253447"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 4711451,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "1c82823b00ec24e20097a71a405c8ba62d3f3ea24aeab269aee9a94e224e2874a79ceb9d42fbb055b7b9bb84a6815272e467a92b0cb9adf83b1386cb6f71fac6"
                            },
                            {
                                "filesize": 29400808,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "c8ee359346b9267a05af0269e45e8c31b80c59177d53da952884cf93306b634a05c59156713959bb4c79b29f494799bd3ad9c74dc198ab9f0333c4d99af2b930"
                            },
                            {
                                "filesize": 27767708,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "4453698193325a9d9a5eb6633c9e1a44a5ef2de26ea1fa09e6e1c4765c057cbf8d0248b5efa15a6393a0cbee93d8badac1ff0ee9d6989fd87a57d2075bcc1d40"
                            },
                            {
                                "filesize": 21476448,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "a39d7a5aed6f4261e95d85e1eb52b1d11efda9f33d2c7defd5bbdaa4a80363443e8b9219526b7a8f8e3cfd18ec096ee97881c57e89e7d77ecd250dd740a7a65e"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "vi": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53464221,
                                "from": "*",
                                "hashValue": "59db9d095fe6918744175a0ea4930dcf5e137ebc11ac667c8c0f335429d63fe7458011f343e912b40b360aaa15a90046ce829ef464c869adffec5ad81acb066c"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 4711491,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "f3e02bed48c39d7961392ea6ad8502f3d45fd06a31ce33da501a6fdfbf48fe90f1aabccd715c66f1e57f93e756fdae76c0326ca7745b87a524cf8536f2f05c6f"
                            },
                            {
                                "filesize": 29396219,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "357307fb48a91ad9595c78d0ae6e1f815f0fb7f8a2bde5b203d8a354a162f4517d254f321c818570528f931c8e9f83e01e0da6bf1df28267d8a1f3e23cc574e4"
                            },
                            {
                                "filesize": 21496523,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "4dc264c0d9bb3b588bd9d9e65fc352fbbdf5c7afd686f3b8d6cb2b17de458ae619475eb60deb9c15038b461c4b4fa0809eaae1d72febc2dd5c2f99a495cfef6b"
                            },
                            {
                                "filesize": 27768770,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "f4aaaf531c93d17fff037f7226a6136680b8261709b6300cbd5c66f21b0427bc411ab28df235909137c8b73f93a88f6f1f9e35eeccc64f54345e35715a6478b5"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "xh": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53415968,
                                "from": "*",
                                "hashValue": "49ce237b570fd4760088a9b8c68aa9ac454935ad9fa19b5e566bc52ce6e6aa5ac438dd8f726bbfc8a832d35e5c7d1b2f7502d8701660218dfd5a354c624626f2"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 29442682,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "c712903e4d1fde8c495fabfcef873bd7828a01d5a89f596d4574588771e83b77ecbc9bfe8c31e92f92f86b05513f01a5ed95d2e2aa42a77ec95e8f62559e2080"
                            },
                            {
                                "filesize": 27815133,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "44f250fecbbe5446a908b8c410bef668c22f674c3b647a3d9f65494fac9c9ff7e06956fb9b1a43e9cb6f6d936ed4368d83d6dce5ac241e4791b0f94e20e8ed5b"
                            },
                            {
                                "filesize": 4711326,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "b25f65e8d38f32fe751bcf4c17b50c72d07fb54e3ad696deb4af881c7012c1b94d7a39d6c43c98dd8df2d2b21ccfb5a18230e88ec5a1eaf9807b9101fdaba1d3"
                            },
                            {
                                "filesize": 21542858,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "c8e41ceca88a390a10338f7d8909dcdd6440564c1d512e0984660ffb700d29b919a94905e35fc8a2453248fb10d9fdbac27ab7e0f8de7678283dac9c3d5c2ad4"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "zh-CN": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53447814,
                                "from": "*",
                                "hashValue": "5c16a96b8c52116e757b6bed073a8fb52d3c2e17bcc49ced1278261549e436a7e0024478ab2fb132a45919e146838f4f292ff632aea135021b88dbb92c7bcd19"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 27702849,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "b887038fe7307fd43df59e7a9c1ddaf7c9f6169e7247e0a55a83eadeb4ed1dbf894d7472d3ac05e6ec2b0f3e1733d6b8ca3404e435c58d17e47012ce6a2c3da0"
                            },
                            {
                                "filesize": 29357258,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "6000b3e3ffba19773e83b305970783d79f211d650b2bb868e2f206a8b9370ef22d88cf098571bb83a86960493314de508e483fa360fac26c3277ef6ffe994687"
                            },
                            {
                                "filesize": 4711349,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "e98a77599202270a0d7b0e980244f0dd7f01913c9556a12340bfa143138e4922b9fa4de1052f126f2e58bba9252cbf4f011a8880998f51f4407446d6ac5eceae"
                            },
                            {
                                "filesize": 21514102,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "257b50140189596f7f86adf7b86af7bf617b16dc04a8f00f5914bf44ff1da641486c847e39b4616bce53b6f8ee5216b8b1b69e94cd51d9ccdb533998f31d2645"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "zh-TW": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 53666724,
                                "from": "*",
                                "hashValue": "2a338bdc83320067cdd610320f318e8ef3411224ec9844cff212fe9f4b7d9ffd863b0144ca0e3f84a4e1aa04a99c63abba4d942f6d2907cf51144ba79f9f70c2"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 29371099,
                                "from": "Firefox-40.0.3-build1",
                                "hashValue": "16ecf995e901d04abe9f40e47f29e0343039ee981ef36468347bc5d50f81b7f4083ddd53ea57a17478f35dfd86cd207b4d8f41e84072f3f665f36a8508acfd7d"
                            },
                            {
                                "filesize": 4711427,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "b6b83f229dc96a24a361a5803f3432fc51d3f12f1da968a0cef9f162b5776d27590bc9305dc2f80527963accdb551ecae0887505693b51d6410e877574157afd"
                            },
                            {
                                "filesize": 27722446,
                                "from": "Firefox-41.0.2-build2",
                                "hashValue": "21936dfe786c3ecc3f2c7fc02228ab24cac09a9f8ee14423ad0093209a3aacbdefd9e1241461a6bc6948091e236d47a6a24270c99457ded9b492ced244f570ae"
                            },
                            {
                                "filesize": 21540346,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "25d066722b33203046a3f80020e865e7ac6bb26d9d38efdd3b8944e5f2fa3918b6e6daf11e386b3f66e1592265e6e5b60bc3d77b4e8f1cbf78ef4f2c9e0b0661"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    }
                }
            },
            "WINNT_x86-msvc-x64": {
                "alias": "WINNT_x86-msvc"
            },
            "WINNT_x86-msvc-x86": {
                "alias": "WINNT_x86-msvc"
            },
            "WINNT_x86_64-msvc": {
                "OS_BOUNCER": "win64",
                "OS_FTP": "win64",
                "locales": {
                    "ach": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 55779875,
                                "from": "*",
                                "hashValue": "1670f3766880000874a8ae1a82fbfda3066fba7966f3dbbca70d06cddeb974885799e2e5e1442c33558a2e69327d7d659faaba233e40a947de1b5fadc87cec9d"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 5721275,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "7862c10d0c2a47a186f84d53ba92b53eb6b7ef5e270af058076b35a5eeaae25c31417234812e6471b0dd7a61b201d85a28bc949ee1c25fc0d8be31beff4fcbbc"
                            },
                            {
                                "filesize": 23096562,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "c1d78c988cb6bb3b21ee13dbef31698dfa496b86367a6877663139c4a6df1ff5ea7393a8b243d67ec1e4d123739358a96bccff4186f4e474920ce2768adcba3d"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "af": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 55789179,
                                "from": "*",
                                "hashValue": "7dd2e283c07db2cbc8877f78fc6d5ff8471d635cd266f7fea1343673654d06960efaa03c28faeee8b8e876a139be1f1d8b979f41774e1f60a9eec3231275e8fa"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 5721163,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "0f7bdff2ca57962ddb4a72963a10ecdb819765878ff9a78276541e254cf4f53c6bcd5b978a2471036ab2d3aa0805313360bdc484f39c9a98372cc8c419a788e1"
                            },
                            {
                                "filesize": 23048962,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "636170015da869204389de57cbcf5c8c9b1e2778a0ad3554c8fe2d0c5cd29680aed2cd0937e3a60e61873fafadd85b9561f20ddc19e0b36233ed997147511f60"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "an": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 55767279,
                                "from": "*",
                                "hashValue": "ab33554bc2d7e222ca1833ea6ee67af345b3dd6c29d5ed67e7a55435bc924ef05a250096b27f4616fab335798c78d2927fa12cbb424186bbb08bf7d25a82dfe7"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 23048288,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "d284cbd553395492585c42ce8e5b393d5cae38fbec5c943cc99b3b04b5e053fb1ec521525ed4e9013a3372462f464efee9d0206d27435b32f10972cbfc5f35a3"
                            },
                            {
                                "filesize": 5721390,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "b87f3daf86a94ea789c5414dcad8144c816854dd31b036f1d3f43aa32989dbb101cea7a53abb751f40839d26b33a8cf0c0b1f99a5414afd2150fc596729592d4"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "ar": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 55834900,
                                "from": "*",
                                "hashValue": "349f0116e921597e199cee3cd08e5fa37db61503ff421cae7e9f8e4f3efb55d51d5a7e88c1db2c4dc959928f9008ed0635f404247935928194535b9593ff785f"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 5721468,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "8db20cc408746ea522e7ccb312c24cf4b4a35e76ba5f7c70cc0105bd0a228ad66dc245fbf06b7781c7e167159698d41c5474cd64521963cf2b4ddd33a8c7b7ac"
                            },
                            {
                                "filesize": 23038024,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "d661b3d22bb068e407ac1371174e8c38ab5ef3bbbd1250fc5857648b31bc537ac65bc97b45ba87df9d020bffba5903b559863b8a35301707c5d60267f324013f"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "as": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 55817300,
                                "from": "*",
                                "hashValue": "9b7033c1d6a1207210a0e6524387f049b44d2aced62145211fba1580ffb36d123aeab09990813bd6440344af8b6c3f96c74e143596b9c9ff12ebfd41a06bf73c"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 23049898,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "3a2401245bf145374bae91ab6c5ee29711f4178324633ffc1da80b4f2f1634fe677b53363a41173e5e4d06720dab8d92cb9ccfb7ea3be03e7b4994bc4dce355e"
                            },
                            {
                                "filesize": 5721495,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "557e57ffa8534601f114528a1cd678c43ec51af59d0cf2f790effc783f5c7db919534ea8b452b1c9a8e8f9cef8357225f2f35ab3de10de5fe0140c7da30f8244"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "ast": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 55707695,
                                "from": "*",
                                "hashValue": "8c93c32ab7a2fc455541fa4c99ece46f89d90af54d666a9bb4f78f2a364bcc834b071db84383b36caa11415347a357ec8141f7dd04d83d345babcc4f2609053c"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 23021942,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "6ab4fd3e9fef2ffe724057747f139361ba2ca2c908edc3791e1895a245ed6a3513c509bbecbfa5c327c83560de56e41ffc39699b3844c4ccee560ccf33bc153e"
                            },
                            {
                                "filesize": 5721148,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "4f28ade8e1cb7c125f5172778ce0b2f2b06a670bff184535a051713dc886bf55d173843dd37710704de414aebf9c98c5532ac96316fed4761bbdf22cdd8d03b7"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "az": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 55797726,
                                "from": "*",
                                "hashValue": "946d4df7c28e6f2c702ebb850c383e7d850fa4c77876e291b7cbe4bccc525a932288e580ae79bfb30ce7429be2e9d7f5f3a46325e8ddd1e292e56e948b082d6d"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 5721134,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "9e12f7b3fbc903295e60feef54da5639e7cb4b2aad310dd8139d65f08af5cd64f4efcd76a3afd68721989a7b241d04008038da9ee8e7c31fec5d46babdfe8cfc"
                            },
                            {
                                "filesize": 23093128,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "1301eb0829907aa0d4aa740a0052c750b1a72e304426ef03b098fa574b1e2102cb9eab550994d10ee005d7a3e6b00e92c3d18f415f5afe5da259ddfc23539a60"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "be": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 55758714,
                                "from": "*",
                                "hashValue": "30cf86b6f951e5abf348af985fde8059e588fbbee1effc559c038b36c989e5da3cb2cb0f1d84473275d3b0e9ee5a825aafa607c3ce127acd05bdca0501482164"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 5721186,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "5b82d6b7091b216e57359f5436e663011a4af17b765e15a6ea4cfef6b70cfd3e5093d335652369f92fc861709f5ad7d9ba6dd4147ecac9f005f1e3fb2093af73"
                            },
                            {
                                "filesize": 23033734,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "081d1b977b86b162941806da0a472d0b1d3c27db0fc93790691b75f28ba402842662d4828215537fc7c25b1e9184cd6e869c0f4b5315b9f46cd7b6aca22c33a1"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "bg": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 56067632,
                                "from": "*",
                                "hashValue": "b1919f67fbfa671e10e3876b5c988d42aeccfeda911c26c887b7769a7384957437e563c4feeba5e9dc1ef2292d97a1e9e027749b4c9624e26f9ee16584f907a4"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 23117937,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "d1e5d1b7debdf9df3e6d8c94b0d7fe028450e15615301d588110de33b2ea08e5fce9305f350793ef6f84c81e23a98ef31effe7e4e70a7600e66532a287f006b0"
                            },
                            {
                                "filesize": 5721121,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "3d299700b5a7d16fd5bb8c9088dda0c55e13a507fbf4c0bd0cd62d7939fe942217b9ad8ab5d056273fc2064aee65ea8d6813012d1d99cb2adafd1bb479e7ed24"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "bn-BD": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 55845525,
                                "from": "*",
                                "hashValue": "6174f820bff7a189c3da82eba334240c25f70f5911b94a3b892fc0ae328ac68cf433fad21c3d31a3f6a9d0e2f4e5fb16b87b5ab07454e880a582daa7a29dfb95"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 5721483,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "c25da25e341fcc295a8d2619910db4251de1cf0fb66fc6b3bd10874711f3f0cb11fa2077c8e2630b8b65e93d1910e2258fed26e68ea77eee543594387f7f54fa"
                            },
                            {
                                "filesize": 23050687,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "dca799e38dfc71cd23bb06389d5351eb4572b3475a6d498387e71ad932c0e7f5a68567a764e0e2da568d71fa869dc9a212c2aff23e3c137c9838108ad9eb7b9c"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "bn-IN": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 55836201,
                                "from": "*",
                                "hashValue": "5b9b8e1f00704719fcef7ff41dc599274aa5ae7a3eddbefd5e0f4638180f1eb75cf6de779b6088ab7fc37b6f9b8dd7bb258d9f616f1e1646a7b2f3c25051602b"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 23051086,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "d9b6961fa9c68e80c0e3b81684760be003bdbfad81bac2f3216d4ee8b47b36814d8565e41c23f349b4735d046ee3803ba9b1064741148dee102aad577fa5efd6"
                            },
                            {
                                "filesize": 5721531,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "5cfbf746558a5c9f41f4603c0af0bf5be12fbac7dc14e8abb2240967d42ba0c5da6ad3f4696e2cae72cd243c82956f5c5a9941f363584948342ce5cfb6119c27"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "br": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 57116251,
                                "from": "*",
                                "hashValue": "2ef70f59290614205cc793bed4beaa30b69fbacea276045e5922e3a88f296981c3360da6726e692bf8f8dda43fe31b825aa3353e5f9239c97172ebb2caa23749"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 5721295,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "0d27adff9e967e6ff542df6be918f3540fbb01299d17a80c643122a1afe7627b411fa961ca6d293a12bedcfc13f4a4f2b85c09422205d862ccebd74388877644"
                            },
                            {
                                "filesize": 23035581,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "f6e729c937bbbbc6063e461cc5c75c05c8ae1a276add7fcc8c83f5ecec64d00f0ac87a2c5dbcb92587d9eda7a52448c9fbdd853e19e76cc8bc8aed148cffa446"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "bs": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 55785111,
                                "from": "*",
                                "hashValue": "34a05b560e1a9e18560bbcfebb21894fa5f69d466bbc05cbebd5f33ddf96c72c917ade5e3a7fa8c4e30e5c7cb1101f27d1e82d3859cd2de608c8367d393d3fd0"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 23046952,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "f18bfd7d040512be91d1dead3f675c7e3762291f84283a6c9c8e2ae13adc51df35032031890731903a86e72400a913c642917a049f75698ae8e3254a93332640"
                            },
                            {
                                "filesize": 5721503,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "cfe875f27a9062bbf39c7e0141f229c9f2ea15ad5ab815ac33ac590632b2875f9ae23445223be0abe88cb7c75b0bea35006ae87f09bb18173738b332f2e1844b"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "ca": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 56168231,
                                "from": "*",
                                "hashValue": "0053771b78e0dd71b8499a38c6a3382eb570f69c135ea202de0f7a5f0c31ef732220516d72c6b5569be50c7febfc8fd51632b149df58c4dda1c2428e6b21e807"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 5721575,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "7d133d2d5b8cef2161abdf01e2c5bc321e200ad66354731faf91f27a64b726b4e865c9c94ff646541f05f3665f28a5e8bb888a27e07d1da5cd0739c104a7af56"
                            },
                            {
                                "filesize": 23074870,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "bd481835b5179cacaffb9484c699f59ca24c7fb769ac092a4b5f14a3949e02f5eef6754b39aee399e455742d73c16d99e0991161fd6b0255b9d5053be2c5c34b"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "cs": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 55753147,
                                "from": "*",
                                "hashValue": "aa5ad3c9e0ae510cc757581c59020760a7ce7d45c608e79138b416409629da9bf49383da2690ba3e71845aa0d8caa4aae42b9fa7648637985c271ec858943c56"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 23057337,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "827964e19c29ad2495fbd15b066d34f10e9ef15a688f2e54c23f862cc7b93aaa0d8fab87d90a74b8b88e7efd3112941dca97a4bd59d9b47374cbb4dbc0673ed0"
                            },
                            {
                                "filesize": 5721541,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "c4c9b45cb5593e565019875b69cae6adf63811085b23ca879ef294279129d9332b5f310a6217f2fa79bb5191d88e365fdddd26ef67bda22dce40e83dcba5b719"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "cy": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 55748071,
                                "from": "*",
                                "hashValue": "28d5bebd4e4491c63c3e9f147b7495d74bed749b23cde153bb41a593f129a5c31a17401e741f5e307bfa9d367098ac69f647c00332f00d5fe15946a56a254263"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 5721590,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "b36c40e97803204f57c534da1f25b7a92be3680d76b7e5b21ce0648a074d96e936feb0421797d4ee6d45132f9c35560f479347f16a51a2dfadcc732dd29787f1"
                            },
                            {
                                "filesize": 23044931,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "4e2b206939d856e32971ac61185e6602a47fc936e0ae554d9d0fb87602d8a2fefb9be0b8b34fdb4d5f18b09f13ecccd8da707bb5ee6fbf061e105cce9481e1f1"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "da": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 56378408,
                                "from": "*",
                                "hashValue": "8fbce861aeb4969364ff0e677921f15be3a5e99db8bec99dad930457c3de864a0a8550e0e5b0de1696e21f508a819f865ffe0638e863ac2fe7c6208921fce200"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 5721271,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "e9b989082491d2ee1fa7cca60d37f34926980231ef1c884c7cb254290b98c45e8013b2a2e20a84f2c8b7f62767e8e478b67e915170505e50efc4fb11efbdc506"
                            },
                            {
                                "filesize": 23036589,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "179f8f9a780f52cb793be3c5a12a8e5ab2f5f2352dfbbd2cc5a956796bf61e6f0bff2fbac3ca1122e495edf6bee32d4c7cdb043e7e7f83b74e4e4a5840fd7467"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "de": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 55759354,
                                "from": "*",
                                "hashValue": "940cd089c0087bbaf574984ecc419f864809c66badb6d31222647f542d2c298d5eae5309b6d163057b3944e5dddb1577684c60e314a58fd1a02bbb3ae6e354be"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 23046430,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "bf8268c1b4018d45fd9a7b2fed1f548d5dc6eea51067aa37f95bac08174eba218e5824886e48610c8542ce920bd53ab7c0406b1bf3e49c84aa2d301e5d2aeb04"
                            },
                            {
                                "filesize": 5721551,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "574f8f151da5ef78e043dbbe77f27bcacb216b7c8ae93f68600726215f476fdf20d7155b0f90503801d2668038e67c06cc350c72b2589c1ba6cb81361677410a"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "dsb": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 55776648,
                                "from": "*",
                                "hashValue": "fede03eb1dbd8a2fb3dbe1fc67ca6e7bc6798d0f7c821df9efbf53b86c78f8b4971f9bab1a6d8470c807e0db5a51ee81e179e3d1eefd01b478d37130a40194c6"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 5721600,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "42ce59664b43b5a4d264f24e42e1abd85a16949f4c30420e7ad498520d95e10638338205c66940938807551e97a2b72eeace8a418563ac68e9e27586ce5836b7"
                            },
                            {
                                "filesize": 23051551,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "b9b2a79e4c4b08525dbbfaf76740c7129adbfb526a87c16e4ffa4fca3d0919627a20654a78066d393ed7a8a4fbcb27bec9669bf63e0a9f31fd288815c7fa67da"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "el": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 55803132,
                                "from": "*",
                                "hashValue": "ca9dfce15c48f7d42cd1d1eb4b8a5585e1de7c8f65188c9bc9d2267b6b5823a0c124131b0e5bab6c86d5b88c7836df9531b5342ec1d65dad3c4ccb84ca0edf1c"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 5721171,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "e480ef054d6aa24b10476ad4897d7f5eb55efccefd2fe888a7588a252bbd2e6f43fd1965e5d5c4cb47bb64bb755630a0775681ebcd0885175b0f46953f290908"
                            },
                            {
                                "filesize": 23042600,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "52cd63f4aa0c0f3d921d598289bd590a3911f15950648ee60c75ea2cfc546f1cca5341ed0391ef3cccfd80774b160407e6436a56c44aa88421cf86f3184623c5"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "en-GB": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 55737806,
                                "from": "*",
                                "hashValue": "f48c793ca030dbca14650b4882a25ceecac7a26ed430dec6f912153012602937a32cfb99af8b8803c51fe3cbab1a1a86a049d0a7011a87d52e1beb08090dbab5"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 23026967,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "19ecad1d074cab613eae5a1fc69eed08ef0ee8b4fbf36c7d114583b446bda164c4dfc6687d93050525a2080c2806b3faa147901e6af6bbc48794618cdc5052fb"
                            },
                            {
                                "filesize": 5721249,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "23b60dd5ead759f4d7644b5ab4f5ef61a99fdf29e5b24168491229778593fbf10e92454e8a75f459a11b822973776a558ddd740e71dfae04bad59d0c2a77e420"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "en-US": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": "56013248",
                                "from": "*",
                                "hashValue": "fe23546476d6ff60331049fff418179631f82c63050d51c186b0ded43f6bd6509e29a408137ed1cfd142b5235091e8abaeb27b806db1b889acdeeb74fbf71cdf"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": "5721485",
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "3fc11f9b09b5a928f65a62ec801719f42e838b5e9a817f0e7ad2bd723caaf5ff72196586ef6354b07cf91b494b16e5adcce0e2a45b117d1daf0a120a1e2f463a"
                            },
                            {
                                "filesize": "23057461",
                                "from": "Firefox-42.0-build2",
                                "hashValue": "9ba7dcdf0416cd2b4f943b2f9c0ad66c221b687a81c5a0b79d5378f12e89e6f680efc9bcd17156c44d1471872086f42097b95d860969ae6d16e46104e0b8440c"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "en-ZA": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 55745075,
                                "from": "*",
                                "hashValue": "5e41a26be39604b81fe70e4f847d8c031e240d5ef8877db18f43fb0addc4e302e8b5ce600213c80efa68b6a5994ac5c5befa98dfe8aba160e840ca418c4ab512"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 23035998,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "65144b4bd2752e527265735f8caa63ebaed20f13a3e0d6ced0372fbe0aa90d8102b9eebab65721519279da341dcb42769651a2687322e30046f766f15ff2d3db"
                            },
                            {
                                "filesize": 5721261,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "bd96a3c1369f5eaa93388a9a0fa8dc91b4b514fc57836dc4151cb27c44de1c5aec0cf7e1764754bee31b7d24fc1c8f7c25fcc2c4b434495ade97a96af1aae241"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "eo": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 55788122,
                                "from": "*",
                                "hashValue": "742570d0b9bfa105d11328aa20fd7f0c60279a2b72e7835ad8764cd8308d325be2ab6e370c8b879cd35675f19eba095fafbf3b56d9712ecee95f6ce5d674f5e9"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 5721240,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "f76e962ad9e625574bc89031218038d03b85bd75b2fe5fb801dbb07212a34188f883d90f6d45f2c4ff9095e320fe1cc45005d4d5fcf28171c6eb968be221b455"
                            },
                            {
                                "filesize": 23050945,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "7ee4d31966749d06a11374094da8d72ea09c67a3688b466642a0364b4d69aa28e494b3e86a6340893f5a918e9565741569d64bcb0307847b017c874ef2082931"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "es-AR": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 55754396,
                                "from": "*",
                                "hashValue": "e40e6cac0c0618ab72c95f2c048fcecb30769db58be5d9785518531d086b6debe623c55107eea87631f3072ac685e407a63a56a0e27363d2b8383ad14ecb0c54"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 5721256,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "1354e1c00ca4a2dc3109a741c85a107edde4c41e4bbf8bcbf0bd7bde097ab194ca8b140f11e50a417e0d1f0bd9655ef3b37fdb6a50dd72f8163e8510a70e2345"
                            },
                            {
                                "filesize": 23043402,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "9e4a4ec351e3ab2f25ba0fec4ec057a1f728725f0315a31cfdcf04ce3a608929646c8b525550f292701e6043a7441a9d533669e712f3e3c8ec623ac01878bbc5"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "es-CL": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 55678457,
                                "from": "*",
                                "hashValue": "6295ff864da55b16778df4d18d2e84507e48acdb9664815ca5688ea174a4d3fc8f60fcdb193202fb089a53c832a4852c20bf63608b35a3040b628538112a720f"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 5721308,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "39c4b12a7350e17a97f5176aaa80a966ff36d05919891879664beed0a2df1607092b21b32cb7b7ec2be112780fd9ecbc497752c23a9b53d7d1e1ce875fbe4d49"
                            },
                            {
                                "filesize": 23011769,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "836cd24cb5fbb5ed140e6645fbc5d322a7561d127c029dab2f8e4c68724f6a43cc300bbfd9492df101bc90d2e5bd9adfd1c090df42449ff0412ec691057399fe"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "es-ES": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 55664767,
                                "from": "*",
                                "hashValue": "eea68b0c368ae823c310618f3e0ffefc04d119e8b0e6c70bd44f7968cf46bb1242e739a1d3f67aa1b9ef8cbc5e30df539884f81977e32cb4b38247c28554e14f"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 5721258,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "61ac9360ba76e494c7b1975b77119fa0a42ebebce9dd6a6e03a3846c7f2061823d2c4ae208615893fd45484a04b4fa151224a1246dbc19fffc6500f1bda5c720"
                            },
                            {
                                "filesize": 23002144,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "6e6a7706530e3081d4a0fd0b411a573e57d53bcf863a9b8c8932d151e0ef94cfe3fa15a7152a6a632bb89be2d645cc14ccb792ae926f46970e045e14bb3adecd"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "es-MX": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 55761027,
                                "from": "*",
                                "hashValue": "e57c0bd41cf1cb8c57a08e6096e562a8b6ee6545882fcae08da3a89c666b069674e33c0f196f962cec4a34ba4bb52b3096fb032a0acbe7bccac97f63af6bc60f"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 5721275,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "b01d6c05774dace6e7e8c28049fe070bf06304eb90c9c1415541a19c0c1cf1a82ed56d23066e1bfea885f9a5bdc93cb115e0f30bf3a3228d5216ed87bfd3cf11"
                            },
                            {
                                "filesize": 23049599,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "fc9adecb2d2410f5321ea14e98256467279b9dbc23d85fe50bfd7fe7068dc863fb9b3c68579969802ce1dbe85e01c3bb6361a6553a1a4627d6adf7f0c7257921"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "et": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 56587267,
                                "from": "*",
                                "hashValue": "8b6ae98b8a7c416a29a42bd6ea44a3783f575e9c3d7dce354a3f2fd2629b4789754aef590f2ac72fafbfb0880c2772f809d3700695dacfc1d435966705f89559"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 5721533,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "16ddc73aa451c09c398037fcc76976000d9cbe2dcabafef392b25089c283c5c8d772f0b501cd2f379ab9df249f1494d659dea22fde01ef3be0725673a593b0e6"
                            },
                            {
                                "filesize": 23040176,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "647a793fae55ec741198d9fdc3714503a7385dd99a781bdef90473451d28b54cfab4df8084915d0e04738f4971c3b172c4140124775856ee24d19af23b6b78cf"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "eu": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 55772190,
                                "from": "*",
                                "hashValue": "4ac276a051808a2cf88f9b1ad8aa8dec495f0eb61b6f3bb45096056a0e159641226642baacec8f61623d12c8eb09edf929fe8a84d56c42b395ca571d25e142ea"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 5721241,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "0690a67a3c9bbe92ddd0202e13405d8cdafcfee545382ab5b5312c465de6e7188005f5e541af1d2bef8cd95b8811197b02d12cbf5841b67584b480dfb7c57873"
                            },
                            {
                                "filesize": 23047771,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "1297315d3eec36b5b04036b8c884b2f067123dd54bf40edcb7897e03af16a07a61d90f5f5e957f10a33a13d159f7a2f80eba50af6f8716d5b7c73d4a0953b7ab"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "fa": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 55833041,
                                "from": "*",
                                "hashValue": "b83278b729967e9dca7c22d45b453abd3d52559da7e2f05470208e0b0fc59768c5ab7c4ae0c9479ff55b4c57a10ea53aac85bf7e3e6b66494c81b4d1448ec3aa"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 5721186,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "056e2de12143298167f793036f70c3cfa87c27aa30789103dee466d992140c5e3402ebda3bffbeaab921c7e80135d90369244cda71a134e07318b57caafe67bb"
                            },
                            {
                                "filesize": 23146502,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "cd1aa60c2827db5dc1de9ca2fe4a244bfc160738fe92e15f3101da05b700d9f8d95a8fdd215dece68d922f78e80a2921b0a3a30f63c7058b64f7956a4609fec3"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "ff": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 55759717,
                                "from": "*",
                                "hashValue": "5e7f7e9124e7004144cb9bc970cf8f8f3686e6660ad19c499bd969068b904da16d4969847a4957fca3a8e19788ff131341beefe7fe62a6a1ac11a6a9fb7e4d30"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 5721259,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "6ac08621d68a718bb372cb915c49a9f7a8bff8eef0680acdec59c55314cfa36cbd3a267b9adcb7e911226928bc86617e24c5067ce8221e2c027851a3de11659a"
                            },
                            {
                                "filesize": 23028835,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "7f8090c0d59b34feafb2ff2d5410296086107e8670d0446d95459a3e361f38d59c0a76b567e58fd4d8f7846070d8ae93a85fa8f7815db0f4d1c308a75af7820d"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "fi": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 55749326,
                                "from": "*",
                                "hashValue": "3fb7932ae124f36dc1b0dd0e070c61846b15638e9d2ec0ca18e982c6286c218fc46df86dd76a70ee078ca6f512a6aba57a7fbfe6118fff2b376eff834dccac43"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 5721271,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "4f7d78da021d09937c70c29ea047708759b2023c402c4a815b64bc90c2c716467b0f2289721808af951872131076ef5284af640ce3be2dfbf356739f16fd4948"
                            },
                            {
                                "filesize": 23037013,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "6e2285d706b4efc7173f357ff6a56c4d2785fcd7b1ebd8e733ba0cfb4d58a227a0b2fa4e6fd1fd7f4d401d3db46ec2f996b156dfe50992ddfbcde2a1d692b301"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "fr": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 56131585,
                                "from": "*",
                                "hashValue": "b775a5491aa3fe8acb05eeaec2a69f485a3e0eeee7c8ef1882cf3bad91c9705d91adeda1832cf5702422a8bedfe2685b9756487144c98183e63bb08c740bc250"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 23070650,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "050f0edf908e513407f0ab74fe718b5e1e20b98bfe7ebd07a19acbbdf54543be4b930951b0e6458d0abb3452c3967c44db4d7e21f2ce283e485bb8bb7bf23ed8"
                            },
                            {
                                "filesize": 5721340,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "6f4442d0acaf6e3a84b37644fb81863ee801005625e4812005e073daf4fca8b2b14ba4a2512be320ec97cc9191f1df16576841138c22a3bdcbef218b439bfabb"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "fy-NL": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 55758495,
                                "from": "*",
                                "hashValue": "ebf8b47cd9f4bb48d986524a326db37448b71f0f77d0521999b6d1befb20d2d38aff6927d06ef630ac68ed107f545a25e4e11733caa995bbff111c974299be55"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 5721341,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "d49afed19ff04726fb25a5e9054855b7f6f0790f50cdd469aef30e67c0bfe47bf3a413bf10e5723baeccee0cffc4c3f48f0cfa9012f9552e68558a5a18b21d60"
                            },
                            {
                                "filesize": 23055798,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "3447a21a98c09e942e186b412d668c3a972d347886d23076e3a5bc9c0f35a2f03d6f5dfdac72f753a6c96ccc60d0b620fd170efade6e3ce6ed1ed5b35b4a97d4"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "ga-IE": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 55771884,
                                "from": "*",
                                "hashValue": "756d4870f94eb0446b55136e7688cbe56afd0c1970517be6766bbce7a9ddb58b36e795f61c2718ccdf813a978f2ebc20cc32ca8f5d2424d544ce15e082e616a5"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 5721418,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "eda833c76f247d2ad79fb1d3c693a9203f840056bf0387e14ff8206c79393fcc6833247774a376041b0cf4ea5fe6eebfd0089667c000a3cac46bb7a8d3e5805f"
                            },
                            {
                                "filesize": 23054931,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "2c69532936d59b70004d1efc8c2a7dc100955b3e138e594459419af5821a7584601f420680799cb11f658f258758517f091139bb5bc9ed8dc4d9f55e177c3f93"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "gd": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 55758635,
                                "from": "*",
                                "hashValue": "28f800a2fddae7525b33142594ccc05283a236c9321e65639c49836f53c15a21374aec9d560edaee60218bf99509393bb12661602af543fa6dccefd4d39d13a9"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 23045860,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "4ad9fd4e9f769f56468dc8a9ef7d48693455537f2f7d72200c3ddbdfd84037137c30e1f979dd347067005760faf6b43cec5e0b1b78052e5736dc2bf3e74c3438"
                            },
                            {
                                "filesize": 5721328,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "2ca9dcb5b3ceef22e9906d8297f0b8a1d2b7ddb0b57b49519409d1d8ae7ccab0bfb2d892e5c55f126cf0627ad0c4f6f4917205a6101b523cdf156a83d2967b04"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "gl": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 55749198,
                                "from": "*",
                                "hashValue": "630e88a9906147966fe933b4e701df78681b087685ea8c73047eb0db03d5328d70fd46aac918bee307a05d271b3ae6574b288158dc80029e3292d348f9920abb"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 5721610,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "5561a4e52916c8589c70fbc399a2f49c80438c6b6ee4dcceb9bfd10d05926bee4a64addd6cd6a49443cb2f56a50faa25e2426f45453745ee52e6c7f53bb01099"
                            },
                            {
                                "filesize": 23046726,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "2388cdc9ef24eb3c344722a6a71ad0062a17bdfb0e6f149e513011faea911ce074b93061012d1ea5a0466e08b1b19a335e53a41de8f37774843cdeeeabcc148c"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "gu-IN": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 55787552,
                                "from": "*",
                                "hashValue": "be759fa5347845de5c3eed22241599ee3fb5cc9cf68a98a748f03dffbc000030e6ab0733ecae22baa041064b9a070b47aaa1858f53159d1086093f50731a0b36"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 5721516,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "5ab1c863ac8f7a55f5d5e81a0ebcd2a1236255d8cf0b415a83d27de96164eeba812ddd211e020ab9114cce624483b638502b00ff3ddefcffb83e0cc4107853a7"
                            },
                            {
                                "filesize": 23040804,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "6a394d4191d69d069c755c8354d4144ddcd476a2c11bf2c77a404b22ada4e201f0e87d7a263d3810987d1f41266187854aa8f5eacf820282671a8c80d00d4c94"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "he": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 55785795,
                                "from": "*",
                                "hashValue": "84624f05e1f47c657758e1811eaa8ff812db56b2e8f9fab0145272e821aa32a208d46af19e816db1cd12ce3778e745a3a0569a3f5cf652540356928d286075db"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 23048026,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "8f6ceffafb81466a13e7df0565cc10b6460f362c8fce81de14715f0a9f4f9a2ba3ab64e63307e9fda6b6a5d894a8d23e6079f5b94f1ad759575ba76584eeb52f"
                            },
                            {
                                "filesize": 5721153,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "bc2ff160b5df3a5acd4f2e10e7dc48f9b5a8107dd7e6f4b54d9a8faba68240c76486e07ba3592c8984cb31fd571a69ecf064db924d0133cbef8bd1439153928b"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "hi-IN": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 55812335,
                                "from": "*",
                                "hashValue": "cd1dcbeaf1a55c869dd79b88f7b58e667b9919454adda6e066fea502bfe9f5ae4cdb6d5e2891534f6cce2261a9f7668a3714e2607bc9e7421b2a299d21d75f6e"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 5721131,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "6ef8bba9c5f24cebfd55fa3ecf42ac5ed7ab36a31a3aabf46d304bdaf8e88e7e76a519bbfd8b43a2a5c7a09c28bcb82f3b2dd7033965e35d7c6bc73e9f67848d"
                            },
                            {
                                "filesize": 23042214,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "b641c1b7b00ac7de7551ccbab42dd03c2735df547ea6389b09409b639c1c323e17ff0574553922aad361c419fbe20fa74ed99a0b85fded81bd7cc3288e6dad8e"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "hr": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 55784076,
                                "from": "*",
                                "hashValue": "df8c06fa45fde0c299c85393e1385ad95a859894befde87f47ef33bbb81d92770623d43e5b114cf8d977a2e5e80bfc725a349a826e3bdf85c3b467df871da613"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 23047275,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "e4c6384d37a89b576fba96803d3a643af6d27b1f2f01e3596494acccafe3a2de6a70521677e09c3c3a09ebbcc0329990c1830307718a715b218ea158e0e09e93"
                            },
                            {
                                "filesize": 5721181,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "b18c479ced4eaabe0b6319d392704172dec8dd941b7b316392f4af3dcc1067e71f156b67ff0d9fb3fc75f5ca0ebba2666412297685e51e6771ea6713faed3800"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "hsb": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 55773440,
                                "from": "*",
                                "hashValue": "70c329c1aab49b73ff0f0faa9264414e3d22ca424d7cb501171c0f885703e5a6c31c61e1d3afec61c9ea410bd90a875bfbb3516c2fb9c83dbcee17d9a6c905be"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 23051406,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "26ab5d091faf1b1f6b7ddfc92ec60c4bc8f0819300a27e81e3805a6294d4a5f73a36947a7243c9e4d629f327beee1fa53de5e324d2b33bcf99f97f3c3730312e"
                            },
                            {
                                "filesize": 5721191,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "373c5bd0dccd259d42b3727027969e3670cc897aa1523cbbda38cc9cf5f2ffc74df8bba6cf6378750af6cd88d074204b1c9067cc52452a1d966c7ebe3dff840e"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "hu": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 56383412,
                                "from": "*",
                                "hashValue": "c091179e06701a8f2676db36caeca07cd83fc5ca9c4dbabf672e60d74dd018009f413b3d9d3ce7e489dff09e7c09885dcee8d59cfa25b60f8a0bbd92058f49f9"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 5721217,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "a3765e9636e80cc22dbcf0bc44f609772e9e19a6e56664b8ba6eba74889dd0da5bd4788ac926d630f8e61fd4b8a7ad9c3cf6e435a125f1ca0925b574a8275303"
                            },
                            {
                                "filesize": 23046510,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "725c8dc773f9554888fe452bad7808cb56f61679767e36d74351ba56b46c91b5c069d77c3fe9d6b26757ea53928d4287f789515a5c36f6e786af15e8dc8653a5"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "hy-AM": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 55842446,
                                "from": "*",
                                "hashValue": "17591359dfc003cafaa9a66979005a32ec6409ef3d0f1f9fc553e36fa30221476eef29dc960c50824c64ccc450e6f2f56e748ece105fd5badcb2d345284cfeef"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 23030547,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "2ccb11c92bb3feef3647f86ecbabadb1e3f7c413a908651eaca4e23901a39dbd158de144ca4764cca3bad4c3aa86cea3068f75b0d9f752343a38eec0d75f038b"
                            },
                            {
                                "filesize": 5721525,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "cc9ac165bfba59a5412716a1675a8cbf363afceccaea00753d3b4a2ace6e292fa9c7be080ebf479aae81f853b87aa53a2aadf065b9d31b3853c0fce83d66ce91"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "id": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 55828942,
                                "from": "*",
                                "hashValue": "ff311de76e179a06f3832feb177eb8905f3e7fa6681c8a3b80e71f981b5768f6ab490943c07eb3a7408ceea107b845a01ff2631ba71caf93b031d9f02bf00def"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 5721626,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "d299d18beca24dc2f3e8b1a12af13f7aa42203bdf96fcaa3ebd8e92a65002bddd37093896e8a96e7391461b5bb4a487b5bd164d07a18c885e8b4440b79899f3c"
                            },
                            {
                                "filesize": 23030513,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "cb1ab9398cf5cf5f1d682afd4e95c479d0731587324d0ad499d3c0df1ef1a2d8d38f5465fb4a018c13e57458311ead908d776ab7441f7a8661b69fad94ba5f44"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "is": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 55790599,
                                "from": "*",
                                "hashValue": "07f8806db3c2686ed83d639891c24e169cef68f1527903dade01635ae775b4e815c421d867110e5b245320e82b80bdc445ebb526382346fbc14c64383159cb4e"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 5721377,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "0a2f729235c261d7e735cdb0c8eb1c0fbf6cc318a4847d0c33b2e9ab0ceb4c9213d18b4463f7995997257636f4f8799459bec9d77257105320a01c4b9feb6614"
                            },
                            {
                                "filesize": 23044209,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "1a1b20038c97607e377c4153ba3dffe8beec074d5de0f3f8599dd2aad0515903fd2d742f071d3931309edacbb3f10c822221908fbaf4c36e7f5de44ad2b7bd5b"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "it": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 55662268,
                                "from": "*",
                                "hashValue": "a397c6ba0029be5f9573d5bed6ed9e3867e294ead45388d52db4645decddbbf359f36c888299d83eed1fda698f53122ef3f7a0bd602f0321e71dbab936455df5"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 23004495,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "0c6e04044009c50c02f9f4b4fb670e5e67e3189922b242c4adf715ab5025573d58bba4099430e7166b3a9dc4b011b061aa60ec9ec9b15ce919c808a786e5aa26"
                            },
                            {
                                "filesize": 5721469,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "53011934e01f7e3eb75db5c47ec60e369ad2d9cbc52d3293ec2dc1b31584e54aa908a98dc05d429bf7a4e60ab20d4727ba34788ae5dd921e34c90c41ce564dd8"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "ja": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 56021607,
                                "from": "*",
                                "hashValue": "ec49146386e929652bd88e0c9099208d8f6cfd3f1cfc7c5f5c1b9d9923b36e925af6f1735317c9d7f31731632c8826c87988707e9147243abbfa7a7e6b06bf76"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 23053409,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "bd6544d0d97fe5ee3a5de3a6db5285785d5818415ab47c9522a18ccaff39767e5c37a05a7f7eb1fda8b13318c9f7a4b6553476c291f3fbe788eb0acedda081a4"
                            },
                            {
                                "filesize": 5721259,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "95f4dfc9e456624a94e39dd4f2eef44602b21f044b3ac7f836b07f5e8fa0da268b6ace363ee120d0af6f224ec8040e1cebd40d8a5ebff8b5f706687bf8f320c7"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "kk": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 55813133,
                                "from": "*",
                                "hashValue": "bdecbdc30964de46584d73852b477f68c559007f7d4f24301bd54199bc0b5f42213916132e3ec82e1bd7f9414db7eb282749f0c1147d31e09108add1c899a733"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 23127066,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "5f02699c30b3b44e06850fdd6edc4a7b8aa17d0ceeca274c049a2ef15000752951b42117c146fd06ea2d886bfe9ca1abfcb2d86a28be22d24fb9b16521f15b56"
                            },
                            {
                                "filesize": 5721148,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "1fb6cdbafb477d612e4ab700923b67b8f805e7f9278dec05c96071fb015d702f958a40e1249df9c8e5b7e4342094f0edf8586d2f9e7f512d79bfe385eba411bf"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "km": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 56114378,
                                "from": "*",
                                "hashValue": "3bee9ba1e9f3e3c419d31bef4de4c6727b899d6386b19d8920911d222dda9f60b5d67815b2be6cee8585359e6ba1a2eac1692e7ab3b0040870043fa89ba5aaca"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 23068868,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "ca58b9ff4019893745539f0b3f8a303022a705d59b3764e3a9061b2b6b65e0231364198ab394256d9a2111532ab48570080a7cac5bdcfa1f306ccf7768d1e832"
                            },
                            {
                                "filesize": 5721199,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "c3c87a9bfb6197b6bead4a2bc4e3a30ed57e8ecc42c7d8ba081acffcff88af3f5f2a9ce04acae75cc2b12a7f045bcdf1e8f4a067b5d309ef1946eb88568812f2"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "kn": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 55845639,
                                "from": "*",
                                "hashValue": "8a6c116a74236ee871093474bd832fe64e6092f55d84f24a32fb81eb07151fb3f39da41235eaa860ae1714758c532636ae689cf8e1d24b48ba27c086b4bba470"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 5721568,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "62a49e4a9c7ba68196fc937a413d1de61614b902a8aae7d7dbed4ee5d7f513b635b99171f612a9deb3af54854d41c0ebf415bec8b1addaff4c24f2f152310bf3"
                            },
                            {
                                "filesize": 23052634,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "9a585fe3b9a6d06468b139d072f7387d3e5bfb6373fa18c50f8944b3bba7117fb74b16c37a6c93c8c097ac4ed4751af868da188332d7d0739eeb4a6fd6805c2b"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "ko": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 55774995,
                                "from": "*",
                                "hashValue": "4e442eb18d4596a5d1c1d4d2bb1b9b65ec5b9f4aa52cfba52231b0b350a2aa66e394f8d4f92eb4e209674a9d1e41253028cbee3fcf49c9b85b4bfcace3478822"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 23047246,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "ea5e8ed093d01d578cd9147847bae0078b946cb6246a9cf450cc63a1b1c3a7df166fd9af34f5c06510421a45a497bd36613dd9efec3065e03f5eb06a879d4de1"
                            },
                            {
                                "filesize": 5721174,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "1f2af51ce0e3aaabf98c44aa8c97146aedd7482e538c761090b6b02bae3e86ab8a2fa5c501f834a8999f325b2a158ba876447dd673f686324ffc8551a327488d"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "lij": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 55930832,
                                "from": "*",
                                "hashValue": "b4dbeb34db838af011c75acd3547767e9ae71cbf820f59c147c5938ccdc74161681a4845b0531636d5fe7f93e0513a6fed27778ea6505ccf320c32b463da2086"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 23256749,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "b8b2deade35a67b6b1b2b1761b642817dfee38269872455bf7f889d09f6c99a4eca4c14f069e33b34f9b3ec91e5bcf3041e78481fe6372f64d1c7800ef59af75"
                            },
                            {
                                "filesize": 5721249,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "aef76fa5bec7a0c0a327530c7359f559701c9eaeff28094114b1444e4caef136e6a18f8e38d7c833dffb1ff817d44d92a627f1cb17b637d98bd26232459e2ad8"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "lt": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 56114418,
                                "from": "*",
                                "hashValue": "143c078144993675102f2c73953fddbd61208505e622f301d364d3b71d036cfdde9013665b4d327265ec1df1441126b3af694e10b01042d00768994a6c8d848a"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 5721249,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "cbf8ff756431c2cec532cc6318ce44514d29fbca05246ad9c7248b9133f5316d167e210e8cce8771bb022d086f8122a6f91a745dfd2e64b79330b83bf92ebf0e"
                            },
                            {
                                "filesize": 23085723,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "cb84834fb344e06f3e24e3ad620472fe5b790c403fb60cdd74832288513c36ac2f656a4e562b2b0fbe8ebd88f282271c4431195483bcde18cfaf139b1aca4225"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "lv": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 56058002,
                                "from": "*",
                                "hashValue": "1addf3c1189027799dbb6b79bdacbca968bfe218928430859f83eb6488878d41cdb792296d25ac84423f1c3a990290cbf7cce5874a2d529c8fb5cf0beb81a688"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 5721598,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "a883ad5ff535e80aecae077ac5b4d6eae3fa7785bbfc0c16ea493a952e24978570022e402fd9d4925024410a6b58a893834a57a9cca21da52db383b9d7e8efa2"
                            },
                            {
                                "filesize": 23048026,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "8af170fe9ff7cf6f273e240d2f84d121c98c68c7fb917a7e4584cafb1e53909e8fe642078ad63eeb3f13fcea3f8161b46b4c0e4954881e866a8850493048e0b6"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "mai": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 55822474,
                                "from": "*",
                                "hashValue": "8912c96f55fb341c202f679f3b5f87bb724c825b2254e393c0041ff81c6b3371744388019e4026c55613843925ecca611fef89dfa96077ba5688e8fffb16a695"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 23044711,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "e9d140615ddffa4cf81060823254b1003fbbe79ed24530b90c43871aff570c5e27e4fcf51b541d3c0767428b0b9df1d2ced5ee6c9b16725f63a123f6ca21a17d"
                            },
                            {
                                "filesize": 5721583,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "8e22496ba37475c6062a60a0fdb16ffc1fa4c05ee52a5234afe24dc0acd4f076274741062e01118cbc6526e866732cc9289916edbb9bb0d04a0f3a74d60991c2"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "mk": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 56560700,
                                "from": "*",
                                "hashValue": "3f0351f6d451c9661dce91d679a6378ff2573e82ec91d23863dc3e4f8702a2647930fe44217fa6406286caa420a011c06b153d6d4f3b51ca311f69a95cc19691"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 5721430,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "1f748c100a0b297bf818b1f7b391e164dcc2c21d72127b04bb7c43187dd09a886b1fd07a0a3f88d938a0979ded4852324218b8606bc6b16c8ec76fe9c294e0d1"
                            },
                            {
                                "filesize": 23048824,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "015be241a3a3886714d9f210345bb1717c431b2830333a2a63a1b30b3c8dd7c5d105ca2b03f2c2b04660051fbd339fd6ffac4524e3fba5802728d786f2a83b71"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "ml": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 55834061,
                                "from": "*",
                                "hashValue": "07352676a74763a15bc1e1bd78c56c9650154c84bcf0d272436a552422ba9525e7e57554dfdb5c157d79b6aed469085271d68c23881d599c7d4c36d97744c642"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 5721217,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "fda24066799fc56dc2acde1b3b27333e65f23f25bf7ec5ec5f67e20ea3c5022419eac3e32ce477d8dce664dc15f357db5ceced052e18842f1f6506549868da5e"
                            },
                            {
                                "filesize": 23049918,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "79793d232e1bfaa3bf9ed3914b8a47e88c7700912f7789a80dc254281090913eb8e6105377b60f335fc1be8244111e152ed703b7db36468fdc73619ed4784992"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "mr": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 55824619,
                                "from": "*",
                                "hashValue": "0db213b5af1c596adce0bd0e1a62a1c6a221bc0dff66fae22c43c073aaeeae1e56161d98b850207bcdb25682508e5fe449e3c62eed4c129acc18e527c4073bcb"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 23052760,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "a7091f7575e9480e1782f3229b21b9bcb281e911608d4331f00cc3e366da716a3bc9bcea1ffa5f8ad9d0905fb57af38bc64136810cb9c7229ca9a457b93ff491"
                            },
                            {
                                "filesize": 5721396,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "6eae5c6cd6f8e2312c77a4b9c5e796c066dc91824a43bb4008563c77fdb1ba515bdfb3cda11982564f1f3c06f4ecc46a8c030d0c543921ab8c6a6fc837182383"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "ms": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 55796864,
                                "from": "*",
                                "hashValue": "2430bbbd304c75ef00093d7f9431ad8b440641e91fb5271195820ea156bd5a039fae769bfb0e663a7dafd94af95e6ebb2e29e3139f744db860031f8d6927179a"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 5721278,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "68a8785a97e4432c3c40f9236a921fdabebc679bb6e03a96487b642c19fa6ba7d5315051f2789b7332419855be370ada16b90bded3cc553035398b57f0b7515c"
                            },
                            {
                                "filesize": 23023386,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "65a7cfab8dfb641dec34290269bb27b22f9ab2c266e53fc106720e54bb2b89e0f6f1fcefbc27389dde99e642a9a4d90068c3cf27f8651fe2eb3cbebcdc14d2e8"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "nb-NO": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 55748763,
                                "from": "*",
                                "hashValue": "078bf7317bbfb9460cae781caaecdfe0ce5d0b2d4bad7a3a867497090463f6d45acb91208d7f9782037d92a475fc8fd3381f74c7bcc995c93d11fb41f1a58b9b"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 5721571,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "8e411af89df16130f7398e0c027ddcae8c5bd2439a28ef8a6697a52eadda0b6a759309ca639e9a0e27108e74148bfb290a2db66e6e7bd79c57668f8214024360"
                            },
                            {
                                "filesize": 23037665,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "a0d7b08519ea92494178ecb4e58f5e8c0d6ab5d8a6f541d661895b332462cc9914feffb59e45a41aaebd8448323d828723d6accabe130bfbdd024a9bb2e424ea"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "nl": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 56511456,
                                "from": "*",
                                "hashValue": "a821a8411897f1fb6b95b53f94debe39eecaa6f0bb98b27a2683af7f81c3d024fea2e258e837668a147a43fda7e685a04e849c000e80fafe200625f8c6973aaf"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 23050948,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "a6b68b4253788705e2cbe17c74b3a89d1345bb38fae58822f7a8d0583dd4da1177f32ab1f124a06fdcd6a1e5a46c5a386c1ff4242e3b6bfcbe4e399fe84f3434"
                            },
                            {
                                "filesize": 5721528,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "d89e8b3dc7b0f8ecbeaef34625be15312ccc184f4c811dc7f29a6d7848e19dec87e32e8fd3cd2c3ec73426adfd80803dc4eab7c52abbbcc31495c23bc59642fd"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "nn-NO": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 55742618,
                                "from": "*",
                                "hashValue": "168ddb0a227fb5096986f5907d48e04f8f257b3d7a4d454a5cf34f1cd587b2b48ce0d9e72e6ef1ddbaefc1688854813b646070724c48401a21073f6935cc64e6"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 23036429,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "5a4639193bb37891395319185ce2c7fe7a265031d28b9d06264b20a41a6f8f415c53fb0bdbef9ab00c324502b2a3eff5ceb8d7e526f659d6a53751d2c9663056"
                            },
                            {
                                "filesize": 5721423,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "e297f03cb94ae6e18a593ec43770c7c464540886e5be74aff67b167db92dfede9a93effb46a807a4256c03657bbf0a5574a0cfd551e4133bf0a05ae430e24c98"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "or": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 56062225,
                                "from": "*",
                                "hashValue": "24098ce34228906de4124e60725be726e5c7a7fca154c20a066b9bdb1ae7fd61617c27fd9dc5df39213f6df16773f8b64d7767638865c617d1659bb9f8e01f79"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 5721537,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "782aecaba1866c47a41b51d5a02aed20e11204f0577523fe31137b6b4311945b8e27e04b24c87e587038307305b47d5f5e5fb6c293ca86a334d75643992ac509"
                            },
                            {
                                "filesize": 23050469,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "c3d56827924b2a3a79f69ba3ccb60f8142dffdeb67f4f7b541bb975b2ff9645d6e7831f8c7a747be9814fbd34192b9d4c6eec4ef359f12a1de18484900e0b254"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "pa-IN": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 55804571,
                                "from": "*",
                                "hashValue": "0033ed97d97335d667d4cb17a66a8deb8a3070961ba9552146709fb97ccc76ddce8d489ca0859943bef73a5a03a413b2516ed5c41a5c046d7a84aab6cd286130"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 5721191,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "f303e9433ae2cca7b591a9f1a0d5c2dd0423c3012fdb0b6079b953dc53b8185e76d7ecdf2f79d3dae8bb146c5f876ecce40369eb2e2b48ee4a0863e17a77c0f8"
                            },
                            {
                                "filesize": 23046880,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "539e038ccd88f0ea9a3760f2c5e640aaec0520125b9a31a766b6fcd384d6d63d422321abde8702cb4a075091c09641c8eda016d848041f4f0e375cbafac5637a"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "pl": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 56822963,
                                "from": "*",
                                "hashValue": "4fcc909aa7e94211e4f6f05d49bde443b713b263037055678634a0b6d290b235cdd61c84396536d0ca04df211fad605964516ff611c3c2a84294ee4d38bc1816"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 23016031,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "a453a1dd8987e0d87082111d7b0ba8964fd1336b3cc6bea2c9cc2f45143bdea979071611e76c4b4f0f9525aeda7ebc6ba18ede7fda2ece1f486093f6a00009c6"
                            },
                            {
                                "filesize": 5721533,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "5d2a7ecad8b42e8e7110cdaaf05213a37d5bf4fcd8d80093ba398237b7e608e6fd2c7ba2579ce4250cf46a007784086d9abf62d7be7eba5bc643b9ea0b59d693"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "pt-BR": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 55943018,
                                "from": "*",
                                "hashValue": "8319611170a2e19a3b7d4d44b77cfb12ef67b4eccd7e5d82b886fe971b7d5d6ed3166772316cedae3f17e75d1f6d6fdc669d9a9bde1b53e7b3fdc1e078b5d5e3"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 23031211,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "f8e97aa11847c7e76cb8218db642aed89596b1ef62b7dce4d61616b4a2feb8500ab831bb963139a1dcc1bf743d3cba3d5f30262b8744aef49b024c72f74cf633"
                            },
                            {
                                "filesize": 5721298,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "6399d723a24afb9e503c52a360fda00b0983a6febff2ab19a81577ba804d2d6e4176e0d89086e475515ff6e16c953127338f41052b5b46df0c1346cb44cb0fd6"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "pt-PT": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 55933510,
                                "from": "*",
                                "hashValue": "1e83584e98877c19fae57dd29e4d713f565eb456e04011e189357dc2664025927ac48c77fc18003ce75a8ebfa8b7f26e2f1279eefe3b82975111fabde0eed207"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 5721102,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "8c6cea0a46ddff18b10237b03e15f6c249e4410d62ce5371e201b87fb405ca2e2564f56aaed74e8de17538b3aeb8ccd94b46cbdeaef9e0ce26f298d7124e91a4"
                            },
                            {
                                "filesize": 23122148,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "eccf1418415b325eb831b37f9caeb42dde5b2cd01a9584d7d63aad655dd8d7b326df2d6bb148fcf594c80f3262b42cfcc17cbdfbf3b9503b3ad2201afb4ee147"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "rm": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 55752776,
                                "from": "*",
                                "hashValue": "f046edce75329f9d7aaaaa5a2408479372f7d844370fcfc67a9fb7d90975552377a2f339cf5c4fa6ee5caf1ee64108aefd38603e27933a95e5a1023d3c8c015f"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 5721007,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "d3371506717ec68dd1692b845adfec64aa3da5b21ee8074e1b39b010754410a9603be9295c31423003093772fd2c4ef1ac17e39d9c9abeef6667829b30c13803"
                            },
                            {
                                "filesize": 23032039,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "715e25a58b8f775625894f23c279c5210ec1239b3f6b7c57397e88cf061b9671d90da948fa89b97b218cb392a4ac708675b0af5da7abaa2afc5f79d61e64202a"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "ro": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 56436971,
                                "from": "*",
                                "hashValue": "7bf8e1c8639b6a8b4529b6b1f00215139b2bef24b87ec5673276f5ba12f22b75d600f0782cca06361b50d6757f1a688988e0dcd7cd8a1047e4021d997feae2a5"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 5721269,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "4ebb812c5867578de794f0ba398c8c7f318763492f6011c1b7423ef991bfd933425374a1c36052d5956712db55611a8e0cd98029d6d57a661cc38395dc865dd8"
                            },
                            {
                                "filesize": 23058916,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "0cfe20df493797d69d170c8659ef6d81cef0fcae5e0bedd63557ee2f0ffd674f1a5d92ed0cb68e4aa2d9e740e07a0851764466d6825d308105621429353e6a2f"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "ru": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 56236049,
                                "from": "*",
                                "hashValue": "c4c47191c0fc1f510e9cb4038bd03282da172f70c5b054a209dfcf6a56872d3594c73b51d30df568559d81f1d2f800272964b56336c4d0ef8e97900c5f46932b"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 5721080,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "0e67b6ab383105a897d8cb4609d89ecd060a6eed354c8d032f1366c9ee6f34e48d6643e18a553f62a83faebbe5d0569bc27af3098f4b99c5dca3a5e8a62dba6d"
                            },
                            {
                                "filesize": 23018505,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "b56b3e84cdb7b536b3fa2689d4cde87cdbc227552005472433457044a56f691c318015d3f3a8c7b9353f1a76a062ab17ec62013b582c255addc8f47ddec42e4f"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "si": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 55844234,
                                "from": "*",
                                "hashValue": "7a1cda93903f0bba79b56481f6b20127db216b58a54c12c8faa7cf94b124b48c395d13b4219a742b15fbcb85199fbbcc2331737e50c92619d1c4ad6e87d7fa3d"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 5721019,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "17b2d59de418cb221571801857525c1029a045c8b53f8cdec707eaad801b15a0e52c8fd97b962b41a3b57b28db84d63cc38b208dc4773d3ab835c906e78fd201"
                            },
                            {
                                "filesize": 23053450,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "29f8a848267ce1bb6e2c03adca7e65020c880a38ddd6a2df0877a7e87ded101887251fd60a10c0a7e89760a91ab3208ae21a1ae65fd771387aaf6fc2c8c33820"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "sk": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 56674580,
                                "from": "*",
                                "hashValue": "9bd0483b20a33c2bc6355f525445231f55970556c5ea66d3b908520c70bc304db9c32c2114ca0426556789e071e9210c459c354f676668a641abfdee30cf6f44"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 5721519,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "aaca408770cd181be404a4064f6a0c04e319a85e9c11697760693eccf86cab240b72ebacd71ec17485a33a42b8323a89c6a075ea351cf18191eb75a7a8a63cad"
                            },
                            {
                                "filesize": 23052244,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "63260e2f17355d767601bd7294e9c93dcbf56ef52ba6e9804fbe2b7097c4f3b1c23cea9aed6447bbfce220f4c453cdf583ca57e41610f62e51fd7d1f3870a139"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "sl": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 55749010,
                                "from": "*",
                                "hashValue": "9573d613ce3a8881963ce2a1c058f5acfc881419d3c0b0c2f43bb24ad248a99fb78996a5303e1cf73614ec8f09fca927abd036922662e31445082b5ec04de780"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 5721247,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "6ade0844798b14d17e41969def4699244236e6a43792b3c55e7c0bf69d134112c99cb0f1a368032bf8279a768b80f08afd0268fcff25b7b7707a381146abc8ca"
                            },
                            {
                                "filesize": 23041656,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "cc3b6f04cfd786f619485f3c4129a06a956df9a87dd2c8fcb44b9286d50968f235d6b671388d6ec06bb0a952dc1449ed58b18c8f4f9a14af24c934916ff206ca"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "son": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 55754942,
                                "from": "*",
                                "hashValue": "b42015c28a3fc2221c302363f442d1e67fe5c61a7c7c7323db2f86465f31fbb595cfe9b88aeb537417583a0acde6e2fa957032b5038278509806c9e03738601f"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 5721364,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "e04e1f267d59f0881b354279f87fbcaca85866e96b9b29d4fb026211b4303abf30392a1e9174cfbb47c4202511012ed6b5af688e6dd33dbbed34919c79869d14"
                            },
                            {
                                "filesize": 23035621,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "d854f7ec2f6bcf86c3ebd9edc97c0a67595fb26d7046cf83956df1729f8889a818ecac043de5a4c65b37697eb2340e5029af692ab8523be8a38071e4b63cbb02"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "sq": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 55792625,
                                "from": "*",
                                "hashValue": "876cede2ee455cfbf2ae386b55c1a4c982d2275223fd9c4e2605f00759ec604e21482ae2b9a9c84c576b77cd0d327f44e622c47de7f1ea3921f9fa33d7495ac5"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 5721369,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "240587c92bfe8171b9b509efb6fd95ae3eb75da2a672c6fd490ee77505f6cd45ea38829abb5a30b99ad3f9ca55f0dd2ae6e891c1a8431feb44f6587ccfd6e47b"
                            },
                            {
                                "filesize": 23053629,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "8d554046fac326d60ee11d6af34ad21c816c155aa83992b22479d4dd340625c0d0c77605b296a328cbefe51a920029494e5037580381156a548b06b2ebf612f4"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "sr": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 57685474,
                                "from": "*",
                                "hashValue": "cec5a8f7ac5027731f3b0834a09fb466a3708a18a0647aac895de1bc3ffc7fb66c975aa8b32214dbc45bf4ce193e491acb070c6afb7ae4998fa620b419d29b11"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 5721336,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "6cf8015d6f1f106878f21773cbe5fa4ce68b5300c1c755aef5e63a73731e16a94b86cf43ca17deacd8728a735407d7a16816967ce0807510b252368be0a47527"
                            },
                            {
                                "filesize": 23045824,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "0ead0f47f74dc914ac2aaf411c9f2f45875bcdacd6fac5b2ceb7d8b8da936a42464c5b77ad3279edba9dc17350ef518371ff4f859adb68d51961854acf7e5902"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "sv-SE": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 56382085,
                                "from": "*",
                                "hashValue": "10ee8b3e3468e822d1f0624e78545335c6146f81962f6df6323edaa79e294f054a02dca3cd5beea5060785fce4a4a6e4949261cc04352204b3b71473d2228990"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 23032106,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "d21ec5a086a5bce00189946ab9d584815855e94be9336c0717102f791dbb6ab93a1f0b328889d5e6f8877f8e39f524284e6482d8531be9432578c39e422bb4fc"
                            },
                            {
                                "filesize": 5721150,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "5d5c1aadc41b0eddb825b6646abe149cf99d1c929709befb6c994a6f7e4b082b095a535112af332f000aef8c02ef8536e2ed6edc1303a34e6f3f519a92bd6d1a"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "ta": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 56071070,
                                "from": "*",
                                "hashValue": "b9030f3fe9c2f557f52fba59f219e5f9ef8017b278ca7fc13cdd22f4407c55a42c65ab5e264644180e65dd89977666b963b50c194cea7beebcd2f0f449d7caa4"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 23042656,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "235adbf17e9e9c720a0d980d6bfbe9b33595805c42dec245615c97963ed55d06368daaaa3f33b01460176a7d9910cd912747d9bb02acce251bf19f09294f772d"
                            },
                            {
                                "filesize": 5721367,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "bbc6cf8510967d46f813a9f8bde1bdfa8df155143d23171a1eba562a89148db936ee4f78f03580dfcf2f353125ecd1432a41e0a33726a3ac8ee9715be5128678"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "te": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 55833407,
                                "from": "*",
                                "hashValue": "3fbee61cf44dceeca26b715a3a8f5971eab8d3208be4598122714f978588782f648571a7be1f17a16781d90a24cad1d4e3d3ea872eb6c1c762c1af7b40734f54"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 23029336,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "519fb0bb2d093ea0a6dc5606ce6668101bf65d7357b040fca011ee7f1b13c64fcc1e69651a282489da84d73275be52d38013c733fe5cc890b02a9c17b1ce1ee0"
                            },
                            {
                                "filesize": 5721289,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "70cabd0c012e9e92ac1f1fcab3c34d35d848963109e1d2fedf7497a2bea1329466163bd0f62dfc6e72f026393dd7cb5aceea491059e2a0f91a5e760dbd4e8a6b"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "th": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 55842119,
                                "from": "*",
                                "hashValue": "ec264dd32c95fcf85c2513352fe3ff94f717b9fa3bd0ccc69d46e6caa63e6d8dd7b1f0e30b11812ba840f28dd6374a3fceffdd599db6485bcf164593afa46e38"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 5721336,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "a33ef7ad3b230b6a45331c12de3d61d50913eb7d9e70d53f1f76840fed76412ffa9f3d67703c6ffff1ce982a7d3338ab514a311145258cc14d87da7335d0edf3"
                            },
                            {
                                "filesize": 23044649,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "cc0fefa5f16dbb15fdd9effade9e7d715039d9ed50038c2d43c55aa07bec50010b325d748780f8db7ec05dcf7dba4e4e4996e7500552e68cafcb1b6b88170b24"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "tr": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 55786647,
                                "from": "*",
                                "hashValue": "c9e29bdc3f666bc1057d584ffb5f2eb280df6c4cea667b04a64f1fc631e83db86564179af8b7a0d1a652eb9e5ee8c670c68a86f852326bf5b85600c9457ddc6c"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 23070695,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "58500340a1b3d744c5e0287711c2df5ec12f956bd514661973d82fcfa8628d91c01f45c603f123fffdc3922727964357821ff1fbe52762038ac8bceeebfe6baa"
                            },
                            {
                                "filesize": 5721542,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "1622dd05dd36f196f65f65b37088b972d8ef9fef15ff4c9da6927fe73cb4381adec6e371ee45efcf6d0e6f1ed4cfc3476a9ae81f5ee133e9460a5b317ee1c0c0"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "uk": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 56232353,
                                "from": "*",
                                "hashValue": "a7a59a0904598892d5ab7c20bf8efd20e215246dfb39275dd980c1dfcef26eb332beb871cc7532f322b1807292af15a505bb1c63ec89cbb595e7fc88addcb67a"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 5721259,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "fe904d0db86f2407e49bd55e42b055e3fc9f60fa8f8ad488abee38f0987a04423c14dafa3bb5e2175fd12115c0665d295395ce55c222e56ce3275234895f74e1"
                            },
                            {
                                "filesize": 23072933,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "d014e07c1087938a444c8babb1f3d50722365b29e1cd665479731519cbaf4ca9e1841cbdc36414eb6d4d1623972a0975d4040d6d66e3ade8e086cea420cfe46a"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "uz": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 55805057,
                                "from": "*",
                                "hashValue": "4dbc4d5965fa6d4c3f12cdaebc277204e5e2d3c424661bef6aaff3d12c64ed80b1569a7ecade2591174d1105c64bb31e849935be330baa4dcef7d189ef2a6133"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 23020766,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "f6da69ffc359cbf3d87aa49954e4b853c17c586145cc37d226c67c3f865ca13b269bbf5585eafe404835b3e59daf79e51f521f32039e0a2c83b6977b325aa3e5"
                            },
                            {
                                "filesize": 5721255,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "638e7be659e9b36fdccbeaadbb39c985e3c57010b1b2ee7b57a117e2bc5f82613af2132721ecbda75f0938b11fd6ace5feb7e3605f7b72326113073bf32307b2"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "vi": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 55801397,
                                "from": "*",
                                "hashValue": "cc3b29d2e07a21900ac067e344e19b5aee185e43f7372453d6b47f73813bbe1bffdf1ec03be1f2e8862bf18761da386dfbf3a4bd1e14b3fbde8f54e8326240c1"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 5721380,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "7aed3713c80361f9503bf316eccc284ec8d8d475314818288c29c6bceef8d5115832b1c942e8936f7d73214461f028327487e37540dd6bddb6d24a27c934680d"
                            },
                            {
                                "filesize": 23041341,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "9982324e5a1ef29b446fa9c48387a4fa0004a0d9ebde75bdfad00cdb174381bed783e1535f054379f8227b58edcf15c0635d4cd57f472f205031c97147337c6b"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "xh": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 55753813,
                                "from": "*",
                                "hashValue": "e7308e036d6eec5827f93abcc27ad32a76ec405d1ffbfa5f6a80869c7880db1d0592bc67a947ed985b3d54b1549342762a1efec9ab8076673a4adae258b35768"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 5721339,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "5405b78213271d27e23b68a8945bc458e61061392ca6e72cbc4a2d372b37556c43c66f9163837a4988172626221a285296607ffbc107a1bef67bd279a844f68b"
                            },
                            {
                                "filesize": 23087619,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "1ed9e97c5074fcfd410f41a47c34087bfd98c138e81a0e28b1b818b6f177ed5c8822d5c19816d95af5dcf6ada904e7bb72d97b14b88e2660bb285a0eee68dfb1"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "zh-CN": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 55786149,
                                "from": "*",
                                "hashValue": "c11d98d42afd9c5fd0761db44aa28e69168e941df969413d50bc53bb633698119f8e5efa90492dd02b9994da6bab78223f2f4b89a8965aebfbdaaa078540b7dd"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 5721445,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "2031207669112f997257ccd3bf8e6ab7861634f6669f1d98389d4c41e51b4bbb94834c297b35fef3bd4a14e720b81e62c487cb04c528246b718c7bd619ffd7cc"
                            },
                            {
                                "filesize": 23059299,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "d8d082607eca9f96f7242cf4df61a96b9ac1acbac8a92fcb7e26bf259e0d3f38ed0400b9adf9c954df29f04f934c593600fc8d63871c059fc72610084ff212f2"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    },
                    "zh-TW": {
                        "appVersion": "43.0.2",
                        "buildID": "20151221130713",
                        "completes": [
                            {
                                "filesize": 56006108,
                                "from": "*",
                                "hashValue": "198c54f9d176360a6c6f28039d3aa58f2926a4dda71447ea1e9cfca2cc41883f7b76abe10c0771ab884c0d6ebecb38ac7fb1c6084da4ae885bf07bff71d38537"
                            }
                        ],
                        "displayVersion": "43.0.2",
                        "partials": [
                            {
                                "filesize": 5721326,
                                "from": "Firefox-43.0.1-build1",
                                "hashValue": "34442df87eb2695fa84934ddef4c8e7da7b3e7b81868ebbc0e1f9ffef20eb2619f9b1656827ad0566720df23bfe625bc276cb09c19cb1517891042fe838d32e3"
                            },
                            {
                                "filesize": 23085008,
                                "from": "Firefox-42.0-build2",
                                "hashValue": "17eca4c09ad3fb8bbf4fb76fb834c0e62d90c69b947263ce83740e88d3b1f177c6b99640785333acd8c185355f03795f344340b498f440bec0c6b587452dc1d2"
                            }
                        ],
                        "platformVersion": "43.0.2"
                    }
                }
            },
            "WINNT_x86_64-msvc-x64": {
                "alias": "WINNT_x86_64-msvc"
            }
        }
    }
