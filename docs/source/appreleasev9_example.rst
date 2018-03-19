.. _appreleasev9Example:

==========================
Firefox-57.0.4-build1 blob
==========================

.. code-block:: json

    {
        "name": "Firefox-57.0.4-build1",
        "schema_version": 9,
        "hashFunction": "sha512",
        "appVersion": "57.0.4",
        "displayVersion": "57.0.4",
        "updateLine": [
            {
                "for": {},
                "fields": {
                    "detailsURL": "https://www.mozilla.org/%LOCALE%/firefox/57.0.4/releasenotes/",
                    "type": "minor"
                }
            },
            {
                "for": {
                    "locales": ["ast", "bg", "bs", "cak", "cs", "cy", "da", "de", "dsb", "en-GB", "en-US", "eo", "es-AR", "es-CL", "es-ES", "es-MX", "et", "fa", "fr", "fy-NL", "hi-IN", "hsb", "hu", "id", "it", "ja", "ja-JP-mac", "ka", "kab", "ko", "lt", "ms", "nb-NO", "nl", "nn-NO", "pa-IN", "pl", "pt-BR", "pt-PT", "ru", "sk", "sl", "sq", "sv-SE", "ta", "tr", "uk", "zh-CN", "zh-TW"],
                    "versions": ["<57.0"]
                },
                "fields": {
                    "actions": "showURL",
                    "openURL": "https://www.mozilla.org/%LOCALE%/firefox/57.0.4/whatsnew/?oldversion=%OLD_VERSION%"
                }
            }
        ],
        "fileUrls": {
            "*": {
                "completes": {
                    "*": "http://download.mozilla.org/?product=firefox-57.0.4-complete&os=%OS_BOUNCER%&lang=%LOCALE%"
                },
                "partials": {
                    "Firefox-57.0.1-build2": "http://download.mozilla.org/?product=firefox-57.0.4-partial-57.0.1&os=%OS_BOUNCER%&lang=%LOCALE%",
                    "Firefox-57.0.2-build2": "http://download.mozilla.org/?product=firefox-57.0.4-partial-57.0.2&os=%OS_BOUNCER%&lang=%LOCALE%",
                    "Firefox-57.0.3-build1": "http://download.mozilla.org/?product=firefox-57.0.4-partial-57.0.3&os=%OS_BOUNCER%&lang=%LOCALE%"
                }
            },
            "release-localtest": {
                "completes": {
                    "*": "http://archive.mozilla.org/pub/firefox/candidates/57.0.4-candidates/build1/update/%OS_FTP%/%LOCALE%/firefox-57.0.4.complete.mar"
                },
                "partials": {
                    "Firefox-57.0.1-build2": "http://archive.mozilla.org/pub/firefox/candidates/57.0.4-candidates/build1/update/%OS_FTP%/%LOCALE%/firefox-57.0.1-57.0.4.partial.mar",
                    "Firefox-57.0.2-build2": "http://archive.mozilla.org/pub/firefox/candidates/57.0.4-candidates/build1/update/%OS_FTP%/%LOCALE%/firefox-57.0.2-57.0.4.partial.mar",
                    "Firefox-57.0.3-build1": "http://archive.mozilla.org/pub/firefox/candidates/57.0.4-candidates/build1/update/%OS_FTP%/%LOCALE%/firefox-57.0.3-57.0.4.partial.mar"
                }
            }
        },
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
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 40820500,
                                "from": "*",
                                "hashValue": "95b567fe339ac855ef31dcbb81b39fa94f8d42604a0764405712da084d2ef4f7a301631191b16fc751c6b48d3149473cd2b8066ef8524a833a448cf2340ffd9e"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 70546,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "9f3ce494bc07f88ad4012a351b338bf4ad0d465c1daf123351850765b4e44341b0642bbf66a344347f904692db590f78e2ad38ffc5979db198f16ba643fbbfef"
                            },
                            {
                                "filesize": 77541,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "32db6d34ce64fbe246a8940ca8339638f975b32292fa28865694eb33a96d27602cb1d476436132d1441739c46f80eed769f29ab44218b43f53fd3f3b08dcf3d4"
                            },
                            {
                                "filesize": 80269,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "9d7594f508fe45dd3afcaedd5e7b41fa85a62485a8bf95aaa6a6d1dba7c730d250cb5e322fefc45f771648542781acdc37c2f4e9805b4446826fb26aedac4996"
                            }
                        ]
                    },
                    "af": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 40820303,
                                "from": "*",
                                "hashValue": "e5e469a6494e10829e4cff06d895b721ff861dbd41b9636b2c51b2e6666a8352f7b900eee0a572fea11611ac6a99187039a88ee6d1257f116c50b42a2f3791e6"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 73754,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "636140b4c74910469e507ea9cb79ad81f931e3d999e090f875125cbda566956177de4f036b2536b105c689a22ad9544ad26cde6a2cc4e93492e0ae2628750aac"
                            },
                            {
                                "filesize": 78009,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "c26b4e32d4d55ce1649f5ef9cf118b6e00b765dd2ab7900cc6d6e5161cf5653655e4982c776eb0fbfcb955ee33125985a38af4cccc0d4db93a526ccdd9efb66f"
                            },
                            {
                                "filesize": 80789,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "9bedea331f98d830a4a786e16d32e9efb9e67cf3bdf57dea3b7728e694189b2c55073a5658cc20c7cef736f48e5df2515cbee5dcee936cd842e17fee8685ff3e"
                            }
                        ]
                    },
                    "an": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 40833863,
                                "from": "*",
                                "hashValue": "701ce0f24f3c30ad195ed360b8118b5a8b89d70ed6813f7a333045226dc676ed90466fd9b010a6f0ef1024cec8a16d4ee817710ee94cdfb215dae7113996e323"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 72946,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "f9eb9c908974ad8b117f9e1879eb5afcd86a702ca43a0ad7f0d06752a17d791c8e88bcf7b3e1f6f9800cec9c8dfc626061fb6e77486f5a61659c960dcfcffc48"
                            },
                            {
                                "filesize": 77677,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "cdbd7c5315bf5b3d087ac9fa5ab7fd9933093654e730e5b2c9b4e6702c70a0541751d623dee726a175469e6e0934a97bdf0c71499d0cc326d5db05320628d9e7"
                            },
                            {
                                "filesize": 80361,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "7cb0899350b73c9ea560963cd224d5dab38d4f259670ab861fbb2e80142f5f5909542560e4f2ac18dbd8ce59adcd4dbbbb3124b5c058f5405f315443c6dc7eea"
                            }
                        ]
                    },
                    "ar": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 40833603,
                                "from": "*",
                                "hashValue": "df1e4b99b891de5038224183302caa5261190f2e9dfece7582437127f9acc431a224ff923a79a232891d696958898465fdf0b505513e2b8269a078c248bc3662"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 69146,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "8374082e704fdaf4330c5b1e6ef891c308fffd8cd6f31cfadfc64fa34e5126201909e28719e5885e7b19a5c00be291c46675478acbb5fffe06bfb695daa3add0"
                            },
                            {
                                "filesize": 77405,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "610044f5c87b787a4fb8183678fcf77ebbf991a7002f5100fa992d2041839f6c1c0f9c01837b22d2db30babb3451d64aff61cffb3471b6dec965255d53761282"
                            },
                            {
                                "filesize": 80809,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "86dead4a51ad4bb1abaec1b85349ce80c846033270046ee644313a9c9684ab1c4952dc8905c25cb4a53d55f196e3b8bc6926a87aa250a22d11c2a508deb2e115"
                            }
                        ]
                    },
                    "as": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 40831863,
                                "from": "*",
                                "hashValue": "592102aca39ae9bf2ae43889fcc8e236a0fdb6840908ce9144989bb8791dbcdd3b3291fd65fc4dd1ddbb1e996312ee10c3f7f267f2354816993d8d792af2aabf"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 75690,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "d6396223d9098dc98265fe9e1b7dfd91b4ff009a78d51cd8d1588bd8ab52bc6a191fdc21d298dfaaea9222b2bb468a60c6220ae05328c1ee424db75d84a6b3d2"
                            },
                            {
                                "filesize": 77565,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "efda10d48a5c3cf03c708938b25477578524219a9b15aacd2dc4146890266d8c32945d2bfaaed513454d8030353dd6cdbc5ddce8501713daa5c504a54149b5d8"
                            },
                            {
                                "filesize": 80237,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "66991bb7ffec0f8850ffb882e0969ec7a0ca3e7003f5141f820acaf8a5b6505a3fe85b1b0af51184e9fe4aeadd49ae930ee82e0af1f59f3285a9d0046645eef8"
                            }
                        ]
                    },
                    "ast": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 40828696,
                                "from": "*",
                                "hashValue": "17e8590cbd250cfe14abc2cb13ef8bdf77eeba7aff7c262fd12cd149129c9fb131c22fe676e439b5e743c29fe723475b829bbb6dc124ea9a743a2afe2dcd4b68"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 71254,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "cea2234facf22ddd84fc1c86e0454c0226a5beb02113badda28bd9c03b9182723332ee1e5f7dc9f638fd8fb6897a3cbc19c904615fcf06de4e4f3e4f1fda96a0"
                            },
                            {
                                "filesize": 77529,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "3c900cf9f862b92a64403bd0931e10362bba64331df8b5190e373ecaa7e3698fe7daaf819cc341db045512c8f11b93ae16ec9f1dbb0d51b07d6880693067d70f"
                            },
                            {
                                "filesize": 80729,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "e124fca4b3c88f6af5e733675247160c428e350f9ca6c54e7face9a22a9b8e987ee572e2690e69826b7a2a74dc79e3fb9a9dc95d6002ca74c8228c0f0d8345f9"
                            }
                        ]
                    },
                    "az": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 40830055,
                                "from": "*",
                                "hashValue": "9b36f97aed1cef0990febe3c7014f09f84a87c5fa5ab070aeda696aaef98980b6acf6ba99f1e1a7e2fd2536d010d0459a8e32839fe00e4f518a09e22ee725777"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 68310,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "e176ab203ffbb6405b6c5537cf65bd326a1658ff0d8458c7aa505d71775559e2263b1f8e39975476cc0cb6dbd9d8d338d60f994afa4664db885df997c725881a"
                            },
                            {
                                "filesize": 77785,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "1564b6847fa0fd81243fa28dbbad9f7b31fca36df60c97a9b899cbfa210f81ff2c07ba7e1bdb8d8a902e20952f39f90aa629f6fab844a1cd7f56555bee4e1b55"
                            },
                            {
                                "filesize": 80225,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "84874c60cee7f94d78e731d164c849289072a761a827d7d134f3bfc1db2fb34666f6ef1cc4a8015c7f3702a8354eb87ce53dbaabcc13efaf3beb28148cb27cab"
                            }
                        ]
                    },
                    "be": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 40843307,
                                "from": "*",
                                "hashValue": "3ce13c8330c58f2c2715529e3c203982cf1e89fc8d9005eba458cfeb67a92e1656ccd6f1cfda22c4e5fd7961324c158c350fd0c314b52898ebae2c8dd732d717"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 73598,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "1256aa258480800197d657618935472e2d7b8a8596dfa98261d61e527fc9e25f939539ecda15559509f79de6055358c9b5eeb09a0ebc87ce2a180ba221134bb5"
                            },
                            {
                                "filesize": 78201,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "c3af3b91c04f33099d0c1a696e67803db561fa7732440d81d035613bb26a181ebb200404f6f0167fbb328532100ebac36915b44f93a1a6365ff2bd172c468a54"
                            },
                            {
                                "filesize": 80773,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "bc595360d249597ac733f9fe5fa3e233ef1a726946c103e6b21ade2e5a7363cf6f8762867abc1163c40b04f66c329d2d91dd1d39d4ed48e2bba6911bda949063"
                            }
                        ]
                    },
                    "bg": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 41516853,
                                "from": "*",
                                "hashValue": "3bd06c54d68d4e779a9fe9b5a3affbdb9c156532a6eace54429a7c829e9d5c9bca51300c598f2fb7e273ae76303a71e0a21649962ac8c7fa543e90ea910ebfaf"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 76350,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "78c16f97498ca12934eeafd4fdb1be7ec1b5be695498457ab0b1be60252725fbeaf5470afacdc562127107ac95bf31d10da0fb74c438beb8cb00eec4741c567c"
                            },
                            {
                                "filesize": 77777,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "42cf823a5676a4047a3fe9c3287b1e9b60e6af4469304219a08531e1ea992d8f4a90635a4095a6b0700cef3645693f6b3f0169305dd64747eda0353f0732b284"
                            },
                            {
                                "filesize": 80593,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "2e2853b574de28cd63b7e42617845fbc7b02b1b2f4f76de43e8a50d762e3ce5b4ff3f117c33a67eb6f36aff2e8915b967bca9f74d1918cf1433fd3eadf8c52b9"
                            }
                        ]
                    },
                    "bn-BD": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 40846039,
                                "from": "*",
                                "hashValue": "4a39c1c2a3413514eea94839a84f071ae6f30a4cb38daecce5baa21a3fd0760c7cdb33d0b190fe2287678f8a3531b86d3b1136d8a3dd98f6e60e1a5c5745d1da"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 75398,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "fb7af16a09f932f633e03fab29004632b46364ac988f5cc81f78e8d9970abb710561f79ac728121a8282e02aaee546a0138a8f984345bbdac4a4681e229ad27f"
                            },
                            {
                                "filesize": 77893,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "31e346ef014ce2116f04d8df452d43f548c6ef8fde70db5937b2b063b823b9c8bc1749d5dabf9fb12a59aa54d1abcf20443c369ea3016705c9a097dfeb566846"
                            },
                            {
                                "filesize": 81181,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "fb23cf7ac1824d0636b6969fdec2fc5178a9a3c6721c8675d28791e8d01574b438a0f1e0ecac558d4c28914921b2bc906e4962ec3e9647718f7a1df1095501df"
                            }
                        ]
                    },
                    "bn-IN": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 40841619,
                                "from": "*",
                                "hashValue": "d0b0b0f92922c42aa9bc023c3f230492d43931d6660b1f937dd4352636f34683ecaa770f6cfba640bf3a921b6497e6fb9da29cbadec4198146a305b56e4eea95"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 74562,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "4f7a0208a511c532ee8ab30bd772d65b92a6dbf583a8a83eb7df1d0ca3775a46d5a96589ee76850bd4560b5cade18acb22616d315da446a17230f7bae9c48f63"
                            },
                            {
                                "filesize": 77513,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "60d8d177af54575ba1d09e3fffb4120be4ca8f57c1780117b4e0ec04eb0298d1c02023df74d760b6d5be10b688e6357e4f112753d752fae9e28d3e4be74f7369"
                            },
                            {
                                "filesize": 80821,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "8c775e19cb822f467561244ee71537ce438cc75d2a1d408867ffa87089ae8bf85010bcaa1b69d112c48214e2c21dd4c5810842acf6eab724f93c5c17b2f4118b"
                            }
                        ]
                    },
                    "br": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 41540229,
                                "from": "*",
                                "hashValue": "4f53ade4196aa80ee1f065ddf4dc1bb764d9d4ff10d13b7b8f1c233999622f3367e74e53d93464de900a31f8670303b3bebfd296704ce805fb0ccba7704ca3d8"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 69286,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "a70324f5dda12f37fb6e4b78cfd1de9d11a82a8b3402c7e339cd614c60cbaf3a2852d1c97b7f2e2001510d64992778642ee603c35742262ec1cdfe4920c18c68"
                            },
                            {
                                "filesize": 77857,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "aa68446e7e6a03ad969d549a9caedcea7fd38f4c826c015b8613568bc19bdf146a534e6f575d0a02d821bfe130814fcae2d12d526d8d4385d301598900e7e738"
                            },
                            {
                                "filesize": 80701,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "267ae3b46cae47dded10f768020199864f8567ea2cb43a75a5163f7f3638d60a828ee056bfb41d5c6e531f80057fe3ed8fcd5e4a1496a14d8ede52e1292da6ad"
                            }
                        ]
                    },
                    "bs": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 40832739,
                                "from": "*",
                                "hashValue": "eae257715ae6c2b58c16cf08c6d26fe8dfcfeba00b3aed107068ca676cc9738370c5c123823918a267926f23e40258e16398331b3138271ba642de130d922669"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 71242,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "bdba2973fa3809b8bee84250b16ea7ab555738697c875ae4e534c4645e18beb74876adfa8b2c69f5d53657fbf09e07b2b64e90e09498fc6226e967cf6920a211"
                            },
                            {
                                "filesize": 77689,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "34614eaa8fa20ed90681c90467be18a26d49ed98eca7876cc9984329812e946ec98cee8b12454b1d236a5383748b7af211141360376bf7cbb0fe9dc32ccdc64d"
                            },
                            {
                                "filesize": 80633,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "9828fb0e3113a69d52db4de16caf07fe782e7892a5b873e005f80176cf80cd328cf73b67244b9f1e7a34bccc1db6259585eb1725c66df2b5326a899233106e29"
                            }
                        ]
                    },
                    "ca": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 41158077,
                                "from": "*",
                                "hashValue": "b9d715496a369a37862df341fa0fd4dd623fc814fb317bdd98f13c6f5b7f4cdaf34ff83b1b413e79b7e2f2d13798d90e6fe61d30cf8d0e79c4f54a130f821f9f"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 70106,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "9816572bebf5595fa5a6b5a823e400a111c40a8792718525926296aa7529dac83bcbd0f55cec45f325176f6914ea0f612a2afa1f7297653045b6c17d98b68371"
                            },
                            {
                                "filesize": 77973,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "06ea03b7318c902942f07f101383bfd8a192c9e99b568acdd20700493ccea0d78541905436214a5919655a25eaa5b8262eee7541795877427445db9156e35bc1"
                            },
                            {
                                "filesize": 80685,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "119366c7ed32a0c0c86cf3e4781f83553412f7eb6007a7b30a739c8febba3469a3b4e938722fe18fb9d2bfa2a69cc7e11626b46ba52fe90cc8f9dd92d2d2c095"
                            }
                        ]
                    },
                    "cak": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 40836508,
                                "from": "*",
                                "hashValue": "7f2260ee6b143258616eae710e5e34120f6715a5de0e0891885b3561fa978a9be98bcd1bbf1f350279a054c73871b7b9e90a8626a9c6b9c4471459335dcb99a7"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 74942,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "b17d8959c6cd21cf6613152e65b0f63d155d8c9174e390247d5c58bef54ae238c9c658cd62f64f279120f20cc3e41a4bd1ea1e5ddd2c8c6ac91cd62da270ad0d"
                            },
                            {
                                "filesize": 77449,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "7e5fcabc00e08e0bf286bdb5ba894e3695f87f6d01cb658ac650b514e59371e7677a230b2a2ded33e84f370bc0257368cd2aa10ba60c86b14bf37146b1a8c4ec"
                            },
                            {
                                "filesize": 80533,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "c5f9f08b2c6599475da002e0bb885b279974bc164d7a9f4f8ea0bcda9bd9d4c8f529ceb92d9c259f531ab7d00768a118a095b75edf44ef71230ccd8c8654d5ce"
                            }
                        ]
                    },
                    "cs": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 40832579,
                                "from": "*",
                                "hashValue": "3744ed9228275aebabf807382907c072201d49f481da92b644df664ce3106ea53d17a6ae8712a9fbed813a7e9b1e7e9b478ddba09fefc732031dea66b7e22a6b"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 71482,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "c42320123c38b54f73e4c945dc26b2a5602aa23df6f0414d92fc1a60a436cfad4cb8e4294f1a2f6faf1003028a1e43c7977e99df8bd869d8c4f30dd3a2bccfdc"
                            },
                            {
                                "filesize": 77521,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "0dea23c32d32fd2acce743b83ab9d44e87b5bf1d80fdf50cd932916f2f1d8eb7654ab71bfad0a0e542ed2f667e540d9cecf99fa3264384313999cbb97f4611b7"
                            },
                            {
                                "filesize": 80853,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "b4e6e72e1234286665a352fce961fb222e033274f8ac3123c0ee9dc9cd8a5e560f0a3972d00d6d14123c2209dab7cdcda8b2eaf29c0bef7a16e9ba565b809856"
                            }
                        ]
                    },
                    "cy": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 40827195,
                                "from": "*",
                                "hashValue": "b70f0d9e126dd39274e52d2f8de8f131573ce49f5d089b546223f003e068fcfb4ccafc4146cb100c6fcfd23508f9120b5d4181b37ae6dbfcb88ff6c0de827cad"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 70654,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "3556de8208aa607defde3b602ae72e87a4a989b3fb3f2329428d918677c1467b8b5c9811b4c7980d3520141f1a7147c45fe36f8d4a224a7d243476e649c5c2be"
                            },
                            {
                                "filesize": 77537,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "3e73e7b1cdbf86ef9ae3d4de90061a88dfa7077b8e0df8826a61d1b4903b8f4b6c1042eda2c03e589a8ee562ff9530200f4f360a01404711947249635e14a1cd"
                            },
                            {
                                "filesize": 80493,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "71ab5d388d4d3ca7828eb27688b3aa49ad597c0b2db581a022e9094c4baf75092804ef0013ef2e93e1a2ecf024759ffb39dfd9712af19ad89e5237639a21907a"
                            }
                        ]
                    },
                    "da": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 41337353,
                                "from": "*",
                                "hashValue": "d32821b8b34a6cda83fa35771a6cd04d35c42975cfe047b27ccd8e98f53ca11a3842e65951179bf993705043c2ce0c7303cc19fd982b88e7515c740055867544"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 72354,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "4e619c3170b4c3eef58bbb32a368c79907646f3eec206a06f70a308a9d4c91226db3af17271fc230f2df62b45e70068ce85c20b1820f0b1620217dbe605ffd2d"
                            },
                            {
                                "filesize": 77841,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "f75586a7f6f173f4595a5ed33fdfbaf4d86363764c2e4b2725d00a8f3865befc13a5fe1c4560207ba5ad7ce5bf214a16366c57840d7d3a17a319940241928e7f"
                            },
                            {
                                "filesize": 80809,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "2db03b6c3715320fa7df6bdeb37137fedda704b4de8465e6c8a3f319aecc8a0834960d889a0bc6a04de7107f51255dc2f06982a0b0cdcab90cc207d2407f8f83"
                            }
                        ]
                    },
                    "de": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 40831007,
                                "from": "*",
                                "hashValue": "968d0ad040e96c771be0e2b1f490db5ca3503a77f5f9f991b7d6980edc43cdde26f7e7849fab127bc86f4567e18d719c667b0089640dbd5bf285dcce8d809755"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 70902,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "d689c2f4a4bec1e63b4314fc3c02604a07a22b73185ae8b951735fcd1a4aee9e1dbbcd821d707439439286bfbc4234e3c9f1e209f9485ca5755a1246817210b4"
                            },
                            {
                                "filesize": 77553,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "7c0ca2f3f03e8c2a33c34db787f73b80be72bd56f793cc8223ef934ff18837fa6bc4151ca6422f439109a09b56cc1039144464c2ce48dd0123b644aa010659c1"
                            },
                            {
                                "filesize": 80765,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "c6a6fdfe0085f9f7f071298411b2c3442a2865b87ea8462ba345b81a63cf40a7e67da1b664fd490398517834003733ab8a97d7a4af09eebfb8ec603c47d91a5b"
                            }
                        ]
                    },
                    "dsb": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 40836268,
                                "from": "*",
                                "hashValue": "891464dcfb17ba3575f59a34495e50be488432db49bd5a3ac4f1eaae4c7bc83ae46fc64dc802dfa0076e31c53e98821d4eaff0069a8b2df04b08be83e96ea875"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 75906,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "9c9b5f2f05ad8637102fcfb55bd98533ec37f6fcfc38c7d03b8da440941346c4aaf33d8e31054602ed076591fa47effeaa681021d64dbba1b15daba48c8090ed"
                            },
                            {
                                "filesize": 77685,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "b3afaac4cc917d0ad52ccb96c896ccf4c3eea736f7494a5a74087c8bbf4e929b27666adfef964cb5ca8051c4628d395760c7567507b18eb78aca6f7e34d0ae22"
                            },
                            {
                                "filesize": 80629,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "a71339701671f2727a773a9d90d7e7a077292d16bfa9e54d32963fa248e7bf94568ddaead60698287190c62e8e8ab9cc57a8faf0791dd720edba1cd32adfbf76"
                            }
                        ]
                    },
                    "el": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 40847947,
                                "from": "*",
                                "hashValue": "a5847fcf058ce9b7717b2ff7d4a7efb3a7da41821bfcfc6c00f05244e8b1022a67e49bce597ae10abcbb025066a9af9d0bc60220292b01e3ab0c42227e588e5e"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 80541,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "8b6859cf6b8b61861bbae5d4af9887e8a97fe0589caa091fd8b4fcb5b8dc668be521b5d33640a06db543ea37292c4d01f9c0e6fc983c7de6af15deb6f513b67f"
                            },
                            {
                                "filesize": 78545,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "bce8055c8abe0c4b457c13c4d90afeb83f36c7ef3cae63e7ba9ac10beea75df872f076263b430a249f83d4851e5f95b422040339033bf5580e1a40551fdd02b8"
                            },
                            {
                                "filesize": 78922,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "33216b273021d8123b3da168c6a4296438266592211d88bc06d2d756b9381978fc3fb951ca4d1e6e93c6e1fd72853c09ba2a1b64aaf15926afa64b41adbaeb95"
                            }
                        ]
                    },
                    "en-GB": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 40809899,
                                "from": "*",
                                "hashValue": "8ca4ecef636bcd687f46a5ee3b6521c743349260cf896633cb6dfae9dd04e2a4cf514df7941b0cf35882edc5280d7750d97b2a9a9c0d051846b171df5288b9d1"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 80545,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "e89fcdf1454dedfacf37563a7a343cd81952ae8ed7ce1071181d29c1b9c2d3f243f6487f415254ad50840d56af48f163192af7db7312d64dbcf162d399b1172d"
                            },
                            {
                                "filesize": 78001,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "1d3713370fc97500487d6380527c93785c4b0f27b9024a9bd34a3b9ee23b26b1f388309af275e70b024bcc8e7bf9e97f374853e8cc5321ccecd9ca195525d72a"
                            },
                            {
                                "filesize": 74250,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "527bfe4ffb424f0aca157fc9f59f6c50acfaffd1ef8b5317e1627447180da39e9e441b4b15f224aa928038874e31907aad8e334bf1e62cec9aa93821faa7aa1f"
                            }
                        ]
                    },
                    "en-US": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 40974279,
                                "from": "*",
                                "hashValue": "d5460915822ba5f5aebd9b8595c40149bfd4978b617d766c24ba2682d8cb1cb7c03abed35e3b75d53f14a4219f64ea59950f98f4869a363d8f752b6239034665"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 79226,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "1209d8f3f3bc116082bfb31f4eaf90a142ea79550e85962e9f5838df7fa66aa079b35bac983d974184b71378912afcd66708f8ecd4bdf9e2e18cc28d1059a611"
                            },
                            {
                                "filesize": 77141,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "bec664b13071e920a8a07a4b00a7a696adba5ca24704c29451fec8fb4699b4e5966e590be43fa1736aaf4f2eb71ac42d2e78d4e70b07a07771165946ed53cbe2"
                            },
                            {
                                "filesize": 80461,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "16b757adac0c242859141a0b101ba10f626292165dc667ceebd2242f4c5d5e38a16fa16ae29bada74cc5c2633314ccd853bd8043778ed11f816733321ad8ac45"
                            }
                        ]
                    },
                    "en-ZA": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 40808831,
                                "from": "*",
                                "hashValue": "5baee013653a75848d8913303c9845b8003cae24ee8858f229fafdc5b59ca9761aaa539e151512d7a80baa0c45ce0cbd884cec8b351a405d0112c1a647f21b14"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 80381,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "6d02db61eafeb282038bca99530f2604d3105456236efb0250c49727927d1db0f1a7c04e6df7614c5e4ad21251edad3567cfb3f773b6a98fac0c84effefb261d"
                            },
                            {
                                "filesize": 78169,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "1aeca065681f4bbc06405a1df2455fa946424a6c53970596b5bb9e1dda60ec0c00c9ea8c7a22bb4a42e423c80569c1fa8c2ceb6efe1637ede97e0f6639458127"
                            },
                            {
                                "filesize": 72550,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "4fcbbc63c0da0837cd765c3047c786b18c325245c9d1d28084d94484da660c488e0589c17a7ab9902a941733ef681c2710d209a495451ee27d37f2bfb3a14c23"
                            }
                        ]
                    },
                    "eo": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 40826763,
                                "from": "*",
                                "hashValue": "b9e2810c06bf44fd101f386e122fd3f9bc903be0e8442de9837eef0414d5ab9953f25521381acf7d5d6aa837bf023a9903dcb7d328f414090dc5b3173e4cbaec"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 80969,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "96164372dfae4e851a0d9dfd32d235b9842aa973624c5f839c6d493783ba08cb0ed61a6a1b96427f2649422bfb4bcfa2a08dece75eac0d4188cf563a65c6d24e"
                            },
                            {
                                "filesize": 78045,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "4b9d19764d240bfda660c7724d044fd038dab5cd993819e6451407d7c87743ca2b64f71dc69b2c9f0e7c640090d982223600bddf8672adfd5ff5041ceeee2866"
                            },
                            {
                                "filesize": 71374,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "fcd608b9f4db68faae20beeea794641d8001dfe34cc9ca5635fa997391074f93250806a3458d504303334d52fc20dc7811374eb39b4906c25d01b4d32c48c3ca"
                            }
                        ]
                    },
                    "es-AR": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 40831563,
                                "from": "*",
                                "hashValue": "360b29ab7358c399fbebb83d54b3dc2bc8da0e97dee8bcc7d0339e65af8bc28e71c6b800cba6cb58895142ff429c4a712fff7175c3868a32f881f59584780df7"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 80605,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "b211b4e907a3f0424afd4672a1dff73d75d689714f7100dfeccc9c4a28835b12ad6cd9580cf18820de0fe5ea1476cf89bed1bd80bb2582dbfc378fc3ad4dc81a"
                            },
                            {
                                "filesize": 77717,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "b07d086f2501a33d8bf8f7b3416d878ba0e7c477571672dfc610ee68062740cff2c6105248f74b2d7f4e760074332e05cba8cec372ffca497235200e67ddc0e7"
                            },
                            {
                                "filesize": 72162,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "77aec7ad8ae30020020ac855192b6ac0ada420a63095052adb270d00a36f8ef7c15b779056c9f9326ba7206afd139fcd8a5623680af179acc1c1f7fc915ff680"
                            }
                        ]
                    },
                    "es-CL": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 40832971,
                                "from": "*",
                                "hashValue": "36402bec170c8cb270a3ba0a680e5d3d1e897f5678bbf53b41cd7b79c0e25dc402dc09a1f39bb8b7315dd45b3c246830726176fdc65c55ac9d36651c5fee2d22"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 80545,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "2db3273f982b83e25bb228d2b2de520d86f41d1a4f4fae19268b872c7ff07042dbf509586eb1005bbd1b1a368d6a5e1c75c1607656bcceb2c86cd06d32bf9511"
                            },
                            {
                                "filesize": 77977,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "f0b88747a19c798790329803275b00f24855decf599d296be6dcfdd66de35bbaab9d7cca47f538cac5e626e97ca6b31b7626ea9c755b275e27f04ff32e6167ae"
                            },
                            {
                                "filesize": 78806,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "1e2d30e235db3d36c5f1c566d70d336accecd95f186220842c69d3144cc6cccc3fb8ee5394aef0dea997166104aab3657343b5f4608b04386391dbd08d71af80"
                            }
                        ]
                    },
                    "es-ES": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 40755043,
                                "from": "*",
                                "hashValue": "910d573bf24e685003044f08330d02ea552511e0234a99c7d750a7d56797a467487550194e27346b65ae5a5ae0778c6bf26b20fc4ec623be5f23878f85d671a6"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 80553,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "d89cefd5959d9be1b5f8c2bbee5ecbf16baea1a6ceedb425e0cd2a881245f10212eff295e49c14e0188b6b5fb2ab1bbcfcbf2358b2a06c932bbac678af38b6e1"
                            },
                            {
                                "filesize": 77573,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "ff85a0091ec971546a594c33c9f2b9a5d3890657e5fa156b2ed8e2eb108b7d2265d6ef0365ed2648ec6396a4561a60eb10461c16ff2fa5a5e5a7ccd123688c67"
                            },
                            {
                                "filesize": 75514,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "dc79f4b617796f310580ec6ed31c40858793565075c6120319af4c4181c62d5e80533e147ea1df46b114f60ee250769c199e498bbe4334cb08a226af9d919da7"
                            }
                        ]
                    },
                    "es-MX": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 40834247,
                                "from": "*",
                                "hashValue": "0d0d1e4463e870b3a2a73d3148ac0b1120ec917f772b8ccda18badd47f4ec89e8fdb39b7d18f200a65513ca80d331f720edc39adcd072aab29d164ead4b1ea36"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 80897,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "b0111a029c7e89f1114d0999733c29762914be9ffbdefd4dac20e427c10d5a0358fdb7a3f835b0111f59309b7ccefe295b1e2c56857ec38daff71b66de3a373f"
                            },
                            {
                                "filesize": 77817,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "4e8e6aef0a2174f214924e52c2a2dc500d368841727884f9adb151b485fe4ec4d0ec7ce9591027d82545ee18d792be9cc60d1648d44f38824b13fa48032b168f"
                            },
                            {
                                "filesize": 75474,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "b62206a803dd3b3f55ac00f5aa8b75f04c72d3de516087a4a8f8635366521d8c4679aa487fe3a248ca805b9cc0b9cd4a424e61cafe2decddd2225dda6d80746e"
                            }
                        ]
                    },
                    "et": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 41454125,
                                "from": "*",
                                "hashValue": "e34fc6cf13650548530a78b43e1c525a5030403f00262c654d1376bc73446f176a519f1a263304accc05e2eca35a2e2e006823d9aaa60b91c9753bc9aa86fcb9"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 80485,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "de80326dbcd08002a046c400b1f3b5731684d22e6c095eb55e8215bfe0f6a4697fb5d2568893f5a9516a35370b2f33d7586335429e99a528f8930696e836debb"
                            },
                            {
                                "filesize": 77857,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "3a0f2c20c3500c7bb1bb7acc82eb20cda1ae30f94b789a0aea2929476db0c4e31308f8395f79245c89e871c830da6544af275825b02332e4f075af41cdd1cfdf"
                            },
                            {
                                "filesize": 73458,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "eb01f4703cb330925a4faa6124fa5f0461f4db7503d8ad60a5150150a75d5df3fb3a959d6f1011e2e762e66c4d8f623d7518f9d3932d020eab03e680b9598030"
                            }
                        ]
                    },
                    "eu": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 40827279,
                                "from": "*",
                                "hashValue": "ae8dcda5237c912169ea3a0b6bab50e7578dbad722c3b2fc797b977896572f00c3bc37e0ce31309dd3b2580bc21a515cd6ce202fcec47e3a246a443457d46be8"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 81129,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "0c45e6c077f958410935ecb0ef03f984694387355c6dc820e651283726d8b19034f37dab1eafe9ea3985a6055abedce63c0f2d01879734b1e01541f267235ceb"
                            },
                            {
                                "filesize": 77813,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "2441a86e72dca8daee2acbd87a9a14552139327bcb807e01e143f370419dc4e598873db5f04c1f1afcfe9a43dc8cea3c4fbaff120ee2e5d4a871bb6de15fd2ca"
                            },
                            {
                                "filesize": 79270,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "bc7d70d7bf3bec404cbbdaac823588f676a1ad0021a833b75db4a76d50689e8fdc651efd3df7a5a20ada29e6b6ffabfa2dae24e11974606c5f83381aa394bc7c"
                            }
                        ]
                    },
                    "fa": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 40841967,
                                "from": "*",
                                "hashValue": "0e47df5f81860e4bc26bb0808ec84f91c118a7e24e9c598399c5c4de8f97fc1f4a2872d11c288ccd5f8539b64a6cefefa6ef4d908e4917eeb32a05141cccab84"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 80905,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "3f972880c8c33d86a91d64e1e61bb91f6dbf2497eb2a0292e409a612f7897315074648b5f32ab6b79ea910faa215a8544c97e3adf6b1e70574d03245c3c0c704"
                            },
                            {
                                "filesize": 69666,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "4d3f9a607f07870feafb8737fd5cf5d9bda134fe5782dcd6773b25af420df5a92fe89a9412845c444ada118e47375d3d04c415c9d3e2367494a749668a7188b2"
                            },
                            {
                                "filesize": 78325,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "59a2e0ffb06beb149fbf53874a5e60a721cd91d8a2120fcddde27951ff335d2387bae3f32fb9c2b9d85366d839c3ec610f3284df2e24a871c6fb69747584ee5f"
                            }
                        ]
                    },
                    "ff": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 40829255,
                                "from": "*",
                                "hashValue": "aba5c78b7421a5ebb06b7fb11fe7b338f497520e2bff7664af67143044cd8e0911fd63ef4e32ebe6b7eac27bbb4bbeca7f3569c2c75467780091f33e7e6a6e25"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 80721,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "70a9e80d45b92fc8d11c421759f40a49df4ee33b901dfd6f5d1079dc8808a97708de9692c7b5e812e1ba1e643b7d82e5f44186fd82b1a1ee87fe1f259f53ea8b"
                            },
                            {
                                "filesize": 78222,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "769bdba2d66f347cb5dda7dbc2aa0b24da022a7e9f0e1994c4ad802f9a6a9fa2af758773f5d8505897dbc4c79bddef8f3ab069e5f2809cf476304c4dfe7d63cd"
                            },
                            {
                                "filesize": 77913,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "24512a6c70c94571ec2068112b788b557ed0dd2a638fe0d63679d9b0e133219b2827ada206a1de552cc2e532893bd56ae38ca60c96961daceac1764d5a4885dc"
                            }
                        ]
                    },
                    "fi": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 40822927,
                                "from": "*",
                                "hashValue": "03e67a87839f3db115b161b0414e0bc30bc3037bc192ce2da9fc453aca86fc4a64fd98e61fe6b73578517aed28833aca038a3bdd082fcd8a966b814ea1956052"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 80857,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "9c899d8aeb2fcf8452d4098a3c83325fab0f81fa52341636adb6e92cd62ec6221b57f7a13558f701a7351bb201e072c671e9ab3f2159162576e9c321214b6474"
                            },
                            {
                                "filesize": 69842,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "060031e7e9007da0c371ab10503f27360ff734a0a00403e543cceb3eb18fd33ccb4cf1efb0b6419edd236f78c50297adcddc697242954b413b14b24de25ebe48"
                            },
                            {
                                "filesize": 77789,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "2033c35da49129e7809dcb3f00cd05297d265bc4aa2a71c98652cffc5d6b13b9e31be746e8f69143cfb8bc791d86e03bfaea0a1a695a0bdc25e20c8f7e340ebf"
                            }
                        ]
                    },
                    "fr": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 41118157,
                                "from": "*",
                                "hashValue": "5ff07b7f21cf66eaa52ab03feaf138c5bbf3deff35723a0d48d8d53d03978548917e62d7944b219792b647a96b00acc50c851c79477e06263d8dfddaaf97f54a"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 80317,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "406d5e577fdc949f706515cf55ec847767ff12aa27378642287c53dd77235f1c17bf116552a081e2395a7b1f44c0db152e033b664fe38f37d4275d04f2f8e6fd"
                            },
                            {
                                "filesize": 73318,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "849524d9300c858c4e23d9418da403ac50738c47e8005a1385a2ee0d4c86f215cf26cb41acd24b46df7b369ee105b77f6639b3f400bd23f4db07858e71d31163"
                            },
                            {
                                "filesize": 78553,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "af8a985ace9d2ca4f75693ca9fd13b2b6b8c37933ce5c0ce9543da30b566f905357de97eda06147f0e815b4943d0fbdcf98a69723c41c45b26c7b59b39d65acb"
                            }
                        ]
                    },
                    "fy-NL": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 42118395,
                                "from": "*",
                                "hashValue": "8ccfcaa7decd5bf8afb818766bfbaf198be92f8492f9a8c2ef20efee89248a0ec99e2c0b38493977c97f19fd5c1260f392d716eb85ee22e1911a253b029da50b"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 80521,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "5c2e46a16cea05399493da608c0669c6b73113b6d6a3acb741f575183b07dd1102ffaa62681164fcb72dc2dd2de969cd61dc701586d9cbb5bcd70eba56e21704"
                            },
                            {
                                "filesize": 73922,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "adf4bcdd7beb01857d04811577aeadde6deea960aed71e1478ddd3c8607e8f3a99e6204001d6ba70d3b206cc254cb04ca5449997ef49081c6c00a8a1dc8a2415"
                            },
                            {
                                "filesize": 77841,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "72d0b560e45ad4c143e9aff80204b95f8ac3ae28c3457ffb7be0c8a287937c1b7b03824ca687ceb90d0e7afd2af1696c2951f2e4186b54ffba281069bcd08c5e"
                            }
                        ]
                    },
                    "ga-IE": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 40836235,
                                "from": "*",
                                "hashValue": "58a8e44a62068abeb149dd4813ee8b0ceb7d9b8047375cb848c876c8dd185260c713b9bbb7818c1a55712cb784573e20b1fffbf965db9755056b58c5c51295e9"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 80405,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "6e6ffc2e9214c2de23f534d3bea9be67ce68f5ef7f57cba4cc5c3064bfecb18f27d4687f5175d72ade88c7c17dbd07bb33f93ef445e0a79caf809d9b35f2160e"
                            },
                            {
                                "filesize": 73594,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "e0184b463ed6dbe9be84d3e0b443721ac8a8812d807b5d40fb4b73b09be899adb9dac7e6d2af747dbec25c1a0805db9d258834dffa1c1e037de7a5125eb47fa9"
                            },
                            {
                                "filesize": 77905,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "fdca00d86e9ed0b055912d909275f333f5419ca7f8576524f2793b3e0d98bba885b106a463e62e9dd7f4f65758423e742a770fd2e2bb2ed9059b9ccf202a3a39"
                            }
                        ]
                    },
                    "gd": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 40828143,
                                "from": "*",
                                "hashValue": "178f9343b9205217c728c63bb279be5c0a66a97a2ed1320006b951587e333755da35b5230c383076b464f6ed34a2fd7bff6265cf19293ca74628695b4d1942a5"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 80445,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "b9f6738dad411c883ac8c9edda9d933adae817e82ba2363f17fa18e65cc4003ea5382f179a4d33947c3f3c573a4254cb0ba7edfe010d0ba9dd8e4a69a20dff25"
                            },
                            {
                                "filesize": 78462,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "e0b15f68cb74d79843deb5448a3d19810febfd4c1ec4e1d4bba8d0e3091ac1532cae9b74e1c30e8dce864427e4425bd3f2548675db0d0539aa6afdb1ece9bddf"
                            },
                            {
                                "filesize": 78257,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "42e5227c64d0268411c1389c5f3c9ce6c03f9de6f0eef76781b575a8c6238e47223c26d14bd5b64fa9de2e60eb4a513dc695295dbddde6e13730fff957430303"
                            }
                        ]
                    },
                    "gl": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 40822055,
                                "from": "*",
                                "hashValue": "2559f85385e0a30f068b2f77eb18d035b9f5c665ffe1665351b3e79adab64733cf52bc636cc0761c9836e4d7587cd94de4d6d255fb39e86b358ae1c749c8b9e9"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 81029,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "ad9df01655c24bc88351c46a9b9546f001cdf869b0416e27c78533a976eb1027540e8c759708f254bd45621f0d35d645d4b3f8e51666026541d835ddd0cb9a9b"
                            },
                            {
                                "filesize": 72442,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "8d1257becb73c05a05ed960bb2d8787e7e1f501c9fb80ed6778db7fc5ba4a5d6e75a34dd70e126096587984d880d5178cb998983de7204e8b90eb34f91aee9cc"
                            },
                            {
                                "filesize": 77637,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "d4c6cdc565cb9e53f824531630c3846795c954e03e8fa57c81b84ddebb96a08f944e49abe3dcb6af869c18dbf8c786a9eea7914f9b2a6317e87fe6a0be190072"
                            }
                        ]
                    },
                    "gn": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 40833431,
                                "from": "*",
                                "hashValue": "620d51618c82fbbd9f74059443385004e6c386e0477e1de0a8be0a2bd8113d8d0c2e9c3dc0f0951681e462a6dee0ab4f33b0ba0e129a0dec37ae9769e4fbcae5"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 80649,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "b9841d7c236f904b253341a7076fdf9f8eb2acd11b87f3c02847081ae66cd43bb162f4a38362081dc3a37c7d0100e6f8c3ebdb083384b389ebbb17bf5f5e81c3"
                            },
                            {
                                "filesize": 79138,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "3d6d1fff7f17a2a502d04539c5dbb210c8dd1a8ae8f937d50b678c06bf6baed7b054cea65a16585154170f46ee1533b35e971a26af79a610e2c1e85543f7c0cf"
                            },
                            {
                                "filesize": 77037,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "03ca423d8665c21536eff2092daf928a232174d5bfbad250b7d8213c44b343c29c067454fda95371f03ed4c77d70d1fdcc89d640cabdac5bb5ee75f24e2fb52b"
                            }
                        ]
                    },
                    "gu-IN": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 40840043,
                                "from": "*",
                                "hashValue": "ec09e29ea2bcff8b33e33154437208b232f484174900448f2bc0ad42edcbceddd814a3811dc81d1d25c00aaa3efb4176a207056589fd7ba036e85a29843a6801"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 80957,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "38de93255e9fc23fb3e4d294beed733bc76286968854cff4f87d4e1725bfa8396540e372d8c2c3f9526510a3e14485e1129c0ac4d30cd8b473faba553f2e59a4"
                            },
                            {
                                "filesize": 73978,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "d141b4d7634dbc4f797ca1007c9e0a127d8f4c297fa447e0b04ce0b6af6a568543838ec3a0c29710e6c69a78d2d48c06529f04de0a238f0abdd111e0859c51e4"
                            },
                            {
                                "filesize": 77961,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "040aacca663a84429483dd106af11b3edb886c3bbefe4f67f4b46baa88d197161a2ab74ad135af75209c1ef4ea90f2c02e25ec1900d3e246d7ae35a8c01e1e56"
                            }
                        ]
                    },
                    "he": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 40827303,
                                "from": "*",
                                "hashValue": "e2582e6d73d618b971aa8273b62dfae1198a787e1552d852c68eaada23152956a7e92ec308bbd2f38640beb8eba633dcfdde84567ada1c5e53eeb6aa31facd5d"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 76618,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "4548473a400e6680686ab5923108f64dc90f802d914388039a5582fc9b7f133b623ee9a3a6085e480378a9b38f2c54c7961bb9fc566a6a4c6d88b6f23ca4a8f4"
                            },
                            {
                                "filesize": 80701,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "4f312eece4fa391f14a6f23278d9e6b61bc75f02c6f016c585adbc09e1c8ac67776a8ae0c6ebc8e03350ceb811f14ae651dc7bed7c369bc554d5cb644c827bdc"
                            },
                            {
                                "filesize": 77817,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "7b4a72e21703e5dbf98776bba58b8db46887d8007cb8ad2d3663a07ff8f4b30436a8444341a89d664edbb0c347eaa7368fc73ae771ef8ff6c27816f6a6223fd6"
                            }
                        ]
                    },
                    "hi-IN": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 40847471,
                                "from": "*",
                                "hashValue": "c562b3ffdc4d1e2d869de64bcd6a16e1bcfc890d199d43da537a6097aaa18ac41212aeae8d59368db16b1e1871b5deca0a90321df069588c7ebcec0c4d0ad924"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 71798,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "8602b1c90d4f8e14d51c352a9da9e1af24d207aef6f3892ff4ab65fe1bf71bc9d149b7d76ed47a0f4f9de71784f39109d15b341be127e1ffe02e748fb7ce1719"
                            },
                            {
                                "filesize": 80289,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "85950f28cf5a3909a20fa52de9c860ac1dbe1f4e10c31dfbf90664eeba936c5336c702a08b119f3b39ddb011bccc00be15d8f710137fa7b0ae3621965760d7a7"
                            },
                            {
                                "filesize": 77941,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "95ecf962dc4249d4fe366895e5e27f4a539b744eb21d3002dd8fc141778b3c51d081bb7dbc5fad791867c75308d467ba783df397993e1628f32c37d6e08ddeec"
                            }
                        ]
                    },
                    "hr": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 40832399,
                                "from": "*",
                                "hashValue": "966df449f927cc4f22ff8b95f3ce6c5888d51b136b8dc62c5f1091704190b197cc00cf49446d077fd864f2acac635358f001e9ce3c68b949fc0ab693a8f0c0b9"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 76750,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "3193b527c00e99df58b0aff3a58213af377667c08f5e2c17e1b68d9fd17673feaf3f289b151c02045b2b39019ce9deb7e834f1e2986f92bc80b7432f63637400"
                            },
                            {
                                "filesize": 80581,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "14dd652dc7d152e0d15fcd7f5b1a021f00e40c81021d50471c287ad93b70b04afca485dd2e947b9769c143927e157ee5d9618760880171e9d683f714d985379d"
                            },
                            {
                                "filesize": 77505,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "7daa227d02b0cbf178951e40c4b17df4050099c7eee9e06b6c12bf6bf644c810efe7a03af42d6167a869ef6423834fed0ebed20921732196e392b0362624b2b7"
                            }
                        ]
                    },
                    "hsb": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 40834216,
                                "from": "*",
                                "hashValue": "56f00463e6070e70c7fccc6eb9746e12bd5c3ad4b6dbd199b2e2d0fe6feb4f504ea0676fccc33e1a15eff85fecaf832cbe920ba2c2d7de96c6b4a11753db5f55"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 72566,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "875bec2edbc2c422063ee46c907d782515b5eb2b435f0ed9d5625a7bff57d2439354a00a525bc789bbc41cd56e3e56bec5f22130f321e1c9c5ce0ab06a53a388"
                            },
                            {
                                "filesize": 80781,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "5e512f613f85e5f15e1254b8d63d123810fe457d2b8c03aac676c45e61c9a5c0044e7d58b6b134739839c8f22bb010b0e169fae718c3659cd1b18c10cea1b33e"
                            },
                            {
                                "filesize": 77185,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "6e83ab1ffff69f44ffb7aa19f3cf0aacdac800fb3cd1f3befeb327bad4467ba94ad06f004b17cbda4b6b9e05ce5eb43cb84ea33444085263e2e4c4c270f0d198"
                            }
                        ]
                    },
                    "hu": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 41385725,
                                "from": "*",
                                "hashValue": "0f94561d3276c9ae7468bc5153e44372688ac6e236e5492fff33d058943a9fb61ee64f12992360f4fdfbe0e804222ee46c4c91bafb5f928b1865c27f596cb3e9"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 73838,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "10881dc5b741629d50f7286b064bbd2cdad647b902629cc054e5885b415b45d8386316e231513be719bd437a78a9e3d2cb2d1ccc894be30c4eae01c946d7cc1a"
                            },
                            {
                                "filesize": 80257,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "5c1a1058d7149c7f4259cffa41d035b9b8b76724c0f2e29f9cc329a7d9e89d732066701e99e094198f61a5aca90cb288a92a0e3767de2802b9acb2f829ee4f23"
                            },
                            {
                                "filesize": 77953,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "7fe31e01f5392cf299fdc71af8561b6553662f49b9377c0f82207ca5b65c73e2adc76a81d65a79e4cdc1a2cb51665f9cb8a4baec5122b4104c2fbf2c8543e1e8"
                            }
                        ]
                    },
                    "hy-AM": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 40841527,
                                "from": "*",
                                "hashValue": "0d52ca30eb49c46648c15ee8638bdfb99f4fae846863bf6fbbfe995554dfa37cbb957349e5dd09866b456604c7569b4bf77dee2ff6492bbd5f19742a41d8de98"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 69510,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "33790180725a8836683725535d1954c6d63eb46bccebe99dea4326610c6be08963817144afe076409d1b13b82328e455b8f07f3e086548c37be38361b6a3db8a"
                            },
                            {
                                "filesize": 81001,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "3521f0c95337ff1fb7bc4fb497251b0c105dab3bcfbd515c1297fa78612bfb2c94d358acd9a306d4af73c38e8ebef52457fe3f98424ba47fe392960825ab689d"
                            },
                            {
                                "filesize": 77441,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "43639db70743c5682c1babc40ebf10848f37d80c2802ba788ae62c6b11990820f6c275b992a9027c1e16b78c21f171c690f0b5d4c006e21587d4bf66660f160b"
                            }
                        ]
                    },
                    "id": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 40917133,
                                "from": "*",
                                "hashValue": "43274462cb23489ecf15e339911d2fbde220ecd4dec7dfd1da788e30b3be36cf1efb6c86ca579ad6bebf6a8ba9880bf6973a20e01f51fde3cc31324a795bd4a9"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 71434,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "dcebb41474db73bda3b5aaae33c91e8e98729f5562accda4ed76f70205bff71a09a5861197a565a343d06a65e7d8bfe219b3ad8157af019f3c0a1cb9f7c292c0"
                            },
                            {
                                "filesize": 80281,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "23df4bf0fa3e00519638a3f0ca00c23977e5b076d75d83a8a1815ca68a72b8ecce210e0838110a91e266455872a7f349462f425009aef40314433f0d1e708786"
                            },
                            {
                                "filesize": 77405,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "02d73dc6d324b754164aefb1e5880e9c0f41eb5be7114b87344341612e485595a470b3d9e5dfdde3591d70d67c6ac5807b096f9dc90793c6b11b6720dd59b25e"
                            }
                        ]
                    },
                    "is": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 40823251,
                                "from": "*",
                                "hashValue": "c144396e5374ec99f3e4c89bf8792c93d5ba24b78b7ac1cd8bb36e1c37c724496203bf2b1c5b73ed9724aaaa4e633c97cc5174a399cc36e568ce3ec41f07e93b"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 71622,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "f67da2729f9a65d4d1f8e6c8176599038e51a275bc13d2f23fcfa480eda23e4a1ad7d2f1bec779f28a045b8981636c452d0236fc46ce077929029e246b66f0a4"
                            },
                            {
                                "filesize": 80745,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "2cf4dc0b7362feb809c2195f8d16a30fe8f05558962a5fe35717e158a6d323995060f043db230a42277e2dfb4eacf9dfd128ab7de3c5f290a1651dd236f3db89"
                            },
                            {
                                "filesize": 78189,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "dc8d4d2639fb0e62ee854b4fdc009d0e5d31f3187198fb69481f83c78e4a498fe7f29e74ede12f4c3cb21c011689353477517772772e5393bec3ff9b94b31c91"
                            }
                        ]
                    },
                    "it": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 40750627,
                                "from": "*",
                                "hashValue": "6868fa130e6f97db3df5f6fbd7109d4bcc5b2de49ac7e7576ccb2697a4bee796cc4d996b48fa895e9244300f187bbe813ab72c7e8b6713d9dc3c96d1475c405f"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 68602,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "4ce4c75a4b467726cf8234a0257e07efcaca9c785f1954d17675a0968e8a2f26b0fc871c1d829fc280e6318ca886d26d43cd8aacf7278229a989e03fa02e7062"
                            },
                            {
                                "filesize": 80333,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "98531c8f7098aa006db62bd20b0307c73e71ec600222badfd07070af0c8b36b7057e4514b3f6632f306f994f7535793c99197b8a7224c5b273528d6a19f5a5ac"
                            },
                            {
                                "filesize": 78005,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "58ee3720d045fd62c23cb11f908b9b41c861e105d338c4da15a5f3cd06ec2f3a788c8a3a4389f5cc2ee83bc762485c8ee97e392f02871bc9411abf74827116ee"
                            }
                        ]
                    },
                    "ja-JP-mac": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 41016059,
                                "from": "*",
                                "hashValue": "ad8762d3ef21ea9b0041cbca22db983a9e28149045058a49906c8edb3f9d982d5fa695d5f1906275f6818dce45df014f0253019f2f82ff16f11efb28723daa08"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 77745,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "c2d24dd742e2407a0bdaf58a81f672fe0977d3fceac231ce7eb3e1f912e0842f92a823df83c4cbd8f2beece9cdc548ca3d454387fc2d1a90c02023e21769d6da"
                            },
                            {
                                "filesize": 81189,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "2cc2015c079f1d908fe6233e3c96e6fd0ed4a301d4e203e144024723242267426fe2ee1fa821b79224ca19ebb3a6b4f3c7f8a263740528a43953cacea71cef03"
                            },
                            {
                                "filesize": 73818,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "23129ab8ef8eaf368b6c17b1bf2ea023539bfe3b7eee4f7e59c27f6120d58c4f334fabe5242af82b6ae3d903c3d5c78142d63546dfdfc99863caad3fcdac5825"
                            }
                        ]
                    },
                    "ka": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 41016537,
                                "from": "*",
                                "hashValue": "2dc32d66a7c4aa9afd9ed923b27c227ec2b42fce4dd9c2db72e9d22789200df6a596e98653217c970d860dd4aac1c24a566f6c52824ac8103268838de83aed75"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 78129,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "4bfd3ce6437ad83d87a5017a235182005766491ddc80b7dba347474bffb04111b4345ca2ab7cb7df541f1dbee7c4ab2918d9b4fbdda55b9edec41be87085520b"
                            },
                            {
                                "filesize": 80473,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "a60bb0e063515bfbf97731f4cfc4e01219f8de1f73bd05a293245b7315baf8fad92f04260ccc8e4d647b937c7203ff152ec27050867bf1975b414db76ba6bdb9"
                            },
                            {
                                "filesize": 76814,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "cd4bfd7f2e9c2046f3662104c805d8515f400f4a68af93b1c28eb5b09ca810105be2c9cc3a90cace92fb7940976592c159a658f3d47b4e73e4c8b3a1f0ae0ce3"
                            }
                        ]
                    },
                    "kab": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 40831904,
                                "from": "*",
                                "hashValue": "1da60dbc8ec6cc35432092c759b5305b4565e132240f1372dbdd50ea0835f1554736b952a82b90db81e50adb0bda701a273c7d2cd774c16a0b8234d3bbaeb4af"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 77681,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "093e51df205e79bdc20a25717600a47cf221f7fb89c7d759452e555065a22c32823f7e28ab1a37322066b7701b95f40cba5711dccdfa492bc6630aa66fe7f692"
                            },
                            {
                                "filesize": 80909,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "8787221b90444e6133d518fb7f7043cc3b9d9dc5fbf0b01f38860cfd9a4cb1fccbede3bd44a1591e582dd1b56cd5df8f1ee4f5b81437c5dcf4a42db47b06adcc"
                            },
                            {
                                "filesize": 79382,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "ee5c18eeff96d5fae7afabb245caaca471162307a9a0051549d5d973e048ff8675f0aaf4a4dcee850916fa83d2ad24a5b30bcc273fcf469da24a60aa3d798517"
                            }
                        ]
                    },
                    "kk": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 40840511,
                                "from": "*",
                                "hashValue": "14cbec7ccca0cffbc61c898ab1d3d335614262e0868cdf3ebddae03561e17b21a63163eb5c4897d68a485f510d44bb303bfc23dcf97f099e497eb68443527e60"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 77909,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "2bd5de5582ed445b06ce9f362efe94f632b821814106b516b0cfdef99555128d58bd512622874dcca55fc4adfac7b7e1a2f675d47ca9a8a1097caef7b5073840"
                            },
                            {
                                "filesize": 80441,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "19c70a711efe73922238ce7bea85689163c1ed6c83745cf062f9f436cb8368f6b78d88ce968c936db82ef707cbf43d44c173da05850d62e2b93e384806c7147c"
                            },
                            {
                                "filesize": 78802,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "109f87d7c5cc18ea07dad4212da4e0a71583418d388636d7560a1b0bfe842104e9c79994359bc38a067e3a1fbabb7271495d4432187758a531b7a88918a21a39"
                            }
                        ]
                    },
                    "km": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 41026171,
                                "from": "*",
                                "hashValue": "6e1caea97aab116ab863f9624441d7857983a50096580a3af8e83975b9c44adb4242dfe4f232e61a0adc7941cedcbd634c61b0bca5a8d66a7f1155eafc5f020f"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 78057,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "62a990c89b4bd83fc4e2c7f0b92bd66362916058ae68d9f6665de34b2c1a0b15cc958f2757163ab0acbd93058b8054abca9f327922bb4289099d36a7bb41e6ab"
                            },
                            {
                                "filesize": 80621,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "57966723b2230b8d6f2cb9c8e7fa950ab3ac1b82e9b5d68d586f30297197a5c7fcf0eb3c7289ed173661182e49cb135a4e0f198f639a3cc83ea422ee1b36fd64"
                            },
                            {
                                "filesize": 74022,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "b068228f02417bba699c9bfa954e859487fbef6ad2f4695e82aa8bb271a3e0ab3bcfeeae7aff524ca174b8ea0c6052293eea9394d62707ac21123f52ae445fca"
                            }
                        ]
                    },
                    "kn": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 40850255,
                                "from": "*",
                                "hashValue": "ad05a42a5f7660a77edd14095774a0a79f2b16c0b1ae20206468c67268638bd838e2cb6f44ffffdf023e6588e563bcfd7290249dc156d0ab1284bd323f20fad8"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 77625,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "284bc09b6eff9844c1206d467371b848da1f24dd903710f956622c1aa07adb4fa6244f8111f533a70890a38bf3d8f444a5f8a536dfa393663e6fbd07fc23887b"
                            },
                            {
                                "filesize": 80853,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "dab58cc6ffb63a1840810769745174451a2b74f819f3e4d0b820f83c588b30ebeb325dc6ad2cf027ee7a4f7bcb1ac32397645767174b1efb6d75da7fa019e35c"
                            },
                            {
                                "filesize": 74666,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "e8b33a2fac0b4ad673dfc03eae375ebbb097e9f4ce3b269758c31b215c43b56089be87c79c992545c0c502046cbfb89f04928e2472694e154b661c97b1fe6d7f"
                            }
                        ]
                    },
                    "ko": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 40827935,
                                "from": "*",
                                "hashValue": "714d96af7414b1864d58fbd3fecae5b7bc418e8ab9d9fba08db67a4e8b9ed4eeb509929562f5fa0d497dc42b0b44b0757981faa4ee52cd964c2fd89088242ead"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 77581,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "0058385e4df4f1d57f59108b4599a8ffe68cc165438dfb50054ee3773757ba87c349416242ca9b9c76d3ffbe29ec0ec0b1c070f75daa6e83c0a981779f246ec9"
                            },
                            {
                                "filesize": 80641,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "4411cd66d618169cd1773c7bf043c73910fdc1f61f39d70f4fadf97888fb2d9cc9d146fad91057ded07f080a6c4816dc6d4883ca08f88c2c919d36df1f65f2dd"
                            },
                            {
                                "filesize": 76350,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "5c2fea1bf46ab2591a28ab8076eaf9fb402e0eb0f7ed443884f396deb6bd9cfc803efe1331c3bf17ad0614654a6844db20e9e7f55e7b23935ef2a02bb472aaa4"
                            }
                        ]
                    },
                    "lij": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 41008080,
                                "from": "*",
                                "hashValue": "3eea62b2cd7ac32af39adebe382d091c11d565d60bd484f6e63bb16e846e1242cbde705236f8b92b296291f032e5602567e7cb858015d0b928af6b8387debfdb"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 78217,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "5d8364e1dae5dcdaf8221290b1c698521536d8b6edd594366d42a219d7423e6522426094373901e680b43397ff994b946508359581dd75941883297b02999263"
                            },
                            {
                                "filesize": 80549,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "df614875e2b65b202a1e29369c195cdf07bcfa3b6c988ae05bcb9d07b5d473be156184605805becc36c24e539d07358cceddc35680b81c5f3ff8b370062bee14"
                            },
                            {
                                "filesize": 74002,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "afce54d3a6589b46051812b5fa558e12a9ec48363032be5b07b62f7c45b92d4b1e8d91efeec0b7111e4dd1d5fb999a79c77e6f9943b84e71387c9990ebafe72d"
                            }
                        ]
                    },
                    "lt": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 41109285,
                                "from": "*",
                                "hashValue": "1be2bee562b7a6db40f2a3970a892a478d2596e0f93dbad67d7bcceff065957c599cfeb88e57d3c33b136b5768ad0ca440c663db0a3c781171cbe04c0e007cc9"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 77877,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "2ab9085066ae01b04daf899187cb340b6287f2ce5496217943612ee1d000d5042be42e0046f78f3de12c70815dbb21114bd20af35cab03875889cfdbbc7cab08"
                            },
                            {
                                "filesize": 80661,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "e34c8e70f483c1cce641ba21e8201a5bbaf05246de7c2d04e4a74f96ed3983ce4d27ec7ee782315b37c6ef801545ad7d1ff1e3ac595b80696ad3333f1e2c8296"
                            },
                            {
                                "filesize": 72138,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "887d3bd2632caa82454d9f2c637bd47751272eb0369678604a917ec9708a5384d5d9aea2b097f86874dc411fe33e7f37e0058218f480ec83703d1313679047f0"
                            }
                        ]
                    },
                    "lv": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 41108619,
                                "from": "*",
                                "hashValue": "face7657173dc0c23317702bfb30fa5abcb5781384e0e24a99e155267f99f270d5f0d47fe479104194b296fa98bde43dd418cbd1dc04f586e214c77fd5eb3637"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 80641,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "273821edf428725784bd4fb011add004889137278f281ef8406aaa53f75ad0ed5cc019782ac7c18868b08d1a52c92641d630dbe3d61315974ef9fa88e8f32fd4"
                            },
                            {
                                "filesize": 72502,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "0c5ee4b674aae5b3b3ceb944fa639a5108f6b3fa008d953999625c794f0ddd7bd7428040704efb09eaf7dc444abe49fd6a698a0c5efb37a5fd862d5727788939"
                            },
                            {
                                "filesize": 77857,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "cb5234a4279782cc39c1a45b9430f0b297350eae790d0cd8eff36c5ee770ac13a14e568e326ce0dd36a5e55a2dd18633752cadd5ec765c7bca37f0fdcab990e2"
                            }
                        ]
                    },
                    "mai": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 40842764,
                                "from": "*",
                                "hashValue": "40705f25c6e377c3fb9d354f04f25bf038ef23b308742026f4742f46b0b7eb2dcba554f027af1e8039a21b87aadeb0ebed422264a8b583fe3f3e6f5a4ad05de5"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 80489,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "e8a3cdf3cef29d422c582ac6889d1da0707265d3a2552d5f1a2a51059090a83b9656bac30cd517abfa24769679c9f6f1b86144b32e58b9e8ad6d3850d56eae7f"
                            },
                            {
                                "filesize": 74782,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "3d7bd60c2f2417a2571be9807f4d2f046cb7b214ad826d2fbca7e6f3040dc5d824d4ce8e02e46dce2fc1fb17d69812008c8dda2086271f5167075093058b6257"
                            },
                            {
                                "filesize": 77853,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "5d29405edff683f6b40dd051173dca23f18a9b059fad35875635527bb6d35b4818e3450bd6bc9e98ae1e4e944720a767f94bc1362f67146f832d3af26f43743b"
                            }
                        ]
                    },
                    "mk": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 41266321,
                                "from": "*",
                                "hashValue": "4b07115bd522da30f50637b3142587ac74a0de997e6e526475fc9534242a7477f6a07113fffde79a8fec01e7770a231fbb8cf53c159a01017187b83bacc0c41b"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 80829,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "819640de05c6a39c7214c105db3fc6ce079c4e0002d75ff2cb9de0f0025d51e14e55fd304acc4ca057607adca6fbfca204f82d77c8825c55ae0401ace5e77ab1"
                            },
                            {
                                "filesize": 75642,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "2a28c36198fc6d2c70b6c5ed77a96cd6febed84ca8d28abeb367d5c1f5a7553e264a138613902eac38be9a6852579b6d473f93dd2c73a9bb94a6ee80a526c45f"
                            },
                            {
                                "filesize": 77781,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "f7d60562993779d10ac2c11d373fc9bd00d7485d75109fc611088b1b237fcd2b0752c78a08a8d10c11e90f2ebd19ee2b3b096d96f0f194898a87213282ace38b"
                            }
                        ]
                    },
                    "ml": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 40848435,
                                "from": "*",
                                "hashValue": "8ea472c8dbc68a7f53118bb5bdcd26c75af6947ef158435c45e3a532152321419f4f9d641c724f16dc45c452b265445b16c4d13f054247ace38f9d622d517645"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 80605,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "3a9b9b348972f0ec2d66ab413e3e4dba557b490fc6e72eb320d292d30a0617064ede9868a2dd75b27e4d4e0803c9b877f3fb069b60865abd939eaa660480e8e0"
                            },
                            {
                                "filesize": 70074,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "9ccf8fcc131348b4defd9a191e3c1045a93c65463f48412e8698ad6bb7be2f424fa9f0ffdbb7bd9c2d048b9aa4e32e9a44c537fb60e4bfe1fe5f4331e0431aab"
                            },
                            {
                                "filesize": 78057,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "5a1ae40f119cd54b700941d9b3ad1c20f6382bf706d2cde155c941b8fb9ba837c29f8242602f986b8508721af92e18604553c4324e9be2fb2d1eb3173d7f2e24"
                            }
                        ]
                    },
                    "mr": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 40845019,
                                "from": "*",
                                "hashValue": "c4c55f7439821b52a8763a6f3ffdf512986d1cbb49432d95d9cf996bbf4bbd7697790eed2fbf06b9e135d4b4abdc72ead803e85fceec563c897ed2b90da2c3c7"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 80949,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "9745937dca3b31e2fd5eeffae32dd5d5e746e5edc26009a5d4b2bcd9980f3be57b702f308231a28ef6fec2702da7d0c5d7314b33189e5cd4ef9a243b84fe5fdb"
                            },
                            {
                                "filesize": 71730,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "37d27f6c405332992f3e051f390a420d256b00a262b39e8cc1d095ec8499d9212e1aa7fc08194f0da5124e00bb52e99f21e919481a74c6fd6d6242a4646c02c5"
                            },
                            {
                                "filesize": 77593,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "14a96a1bc7ca128dd4f3e347668de582b65ca144f12eaec903f57e4cbfc04a0503dfa5750ca8d3020f0ab2b69093bc3bda774d7beb268688a090a1a310c0d450"
                            }
                        ]
                    },
                    "ms": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 40825467,
                                "from": "*",
                                "hashValue": "a615f82ad8fe1e4709647e72fa923b1135d7303928884f8ae05602f6f71751d44fe94d586cd2b6e76131ac0984788fffe282d67abd5e53d6c15b41e2f03996e8"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 80969,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "9b1bdc43554ded96330e69bc4edc5c55415f3bf91ddd0cb5a3711434170703d52f6c5b4cd3bff71075c5ca8523ef80f345ee9d6ae6630b417dd0fe43f5bdfbad"
                            },
                            {
                                "filesize": 78282,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "3977c5a5beda3ecbe59e448300912d029e1a71570b54765ae4c8f91761f2d5fcc9255de5e657d917bbaf38a57cf0a63f20acf3d72f2765252c1f59656ab0ba5e"
                            },
                            {
                                "filesize": 77545,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "379c377569f6f75ce3535e8e017617196f03e3d2ea6a096b09374d5578ba16bfecc4396e46b9e9f08af7dbe35922a75e20e9cdb701aecc2af205520a83308eaa"
                            }
                        ]
                    },
                    "my": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 40848663,
                                "from": "*",
                                "hashValue": "45ac612643807f493fa0393b347e90e18ca40480787bed3cf5635e8f21049e4b90d4f9ef710507af1c575d3e3228d076553adf5af87ecfd7b67c999ca1b23532"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 80165,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "e5ce112d5e08d2ff2001f42a59a8a3ac9cf2ff2c14aa73bbc4f6b9b3ac5786c37921f4ecf38570f4425c5a0e988cd993f42789cc0d1f3defb17cb29fedf7b19e"
                            },
                            {
                                "filesize": 78246,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "f738ebabc44779b371134b364f7d196897898055d7197a150f3a248ae04f1227929cd959706303caf6c0411d79236d1dbb2e51c9b053b12d9c25d0023354d3d0"
                            },
                            {
                                "filesize": 77649,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "eda2785557fc3027379c976dfc6a1161662ab0dd719049ae45462bce7ee44d6bb8358537ece827cf367e91bd08f7262db93dd0c13de98fe087fda3b2b3bdf531"
                            }
                        ]
                    },
                    "nb-NO": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 40824547,
                                "from": "*",
                                "hashValue": "66e848268c4ef61893a9810755a3e566f5e7437f2845616708572e4590eee69e651048afef233f7597b349782f592cc802eda413f2cce000d04ed606c99bce5f"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 80633,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "749e585eba194eefe5de467e9855f06f58fe01ab39af0def54a56a674cfbc7a7df821f459a9f2e608e255a6d673925e7bcb0ab2a0f3500a4048d596bb4467d62"
                            },
                            {
                                "filesize": 73414,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "848f437329f1ec88e01b443f8ab6b2df9bffa1564ad03e1d9652a8d78318c22554206d835349656fb45b4a9f1d1a06ab6f871a4e7c614c52cd02301baa670b1b"
                            },
                            {
                                "filesize": 77825,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "cb7788dd070a1dfd9b83b6b9159e2303078b6f006b102768a19487362fc9c569ff83b53e7d409e47d4fefe86c6bb465fe00e05939ca3bec9f316d92aee1e4cb7"
                            }
                        ]
                    },
                    "nl": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 41499845,
                                "from": "*",
                                "hashValue": "c6dad1f18e0b37dd88a6a7885989e76b9113426d25ed0d9960d25a0ef882814c6ae5a14bfa4f74b6194353d8a217a3861a56dbaae64e173fad6616feef66b6ed"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 80245,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "c472cd332a71fcedfc3472389cf9e04faadbde0009b67e33137d177bf1083e1fcab04d2683cddbf2e3fb70660cf48a737baaf1786e57b927d2d931ee21b5c404"
                            },
                            {
                                "filesize": 69062,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "70e951156901f03dd0735ba55740ded8125bdba2b00d9f2484989a431eb0b58ed7c7b365bc0cd70b7bcf1e6ff9f2c91a20a408feb901921974d2a35d50bb0ee2"
                            },
                            {
                                "filesize": 78105,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "809689021d0e045bbb64d8506d54ccb634f2a926400a932bb2c6cff9d86f14b5f2815aaded55acbd1769bb73c1b6e275a677a8a4402542910ec9fb2d5b3db37f"
                            }
                        ]
                    },
                    "nn-NO": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 40824583,
                                "from": "*",
                                "hashValue": "a42485aa47081443075f97edbc6d05651221fbdc0e80b543411d12167bdebcb3c3d42b5036516992cbc9dd1899958a3edbb0bd999ffccb2cc1ad9bc6d007b848"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 77813,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "6c3b2099346427d36ee26a38fd6c53805690447aa098026641dd062cbe97cf6b84ebf4d0eb234c03ea85104438ed42915c3552ce8c4a365805071f74fc91abba"
                            },
                            {
                                "filesize": 73178,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "56b56efe00f699e7e7cd5d1c8f0208cdb75306383c4c2a5cdebe042ee07525a46ea7adadf4190c7ae70635ffd13d9ec661eb12d48bdb2313d1bc18fec580685a"
                            },
                            {
                                "filesize": 80497,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "e6b7409039508aa399a7289fefd6f73ea179330dfd502776b0bb693d04bd814a6197b74fc466d2e4a8647c8a7c69d56f3441069ec009104c678d0aebfb7b0e20"
                            }
                        ]
                    },
                    "or": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 41011727,
                                "from": "*",
                                "hashValue": "ace0a9e225bd38661ee2c0aad68f64623e6edff04826482fff4e55026f6289a20a60cb66c7421e1906ea35ffdf30b82282dbafb2dee22377c88f547582247587"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 77745,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "6b1e45ccf153b4e69fd932c1b12ab2c64e995f1a7b66b991ec6483948e248a9a29525295424fe9ae0c067272de5dbfeae5f376d2e5d3148f93f15368175ff33e"
                            },
                            {
                                "filesize": 76846,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "58069c945e87ddb29ecbd7ddbf865884a3fa1d606938ec0846e886eff75e6b330a250b7d2a2362ee35adbe24bdff370e38f89ba75a56fe8d4a43bd3515f10de0"
                            },
                            {
                                "filesize": 80377,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "0709612f527c281459b36070833109976710327559dc0c9d289e729111efacaffcad14ca13ecaf962dac66c9b334b23613850110fb7a3e30a296e8be370f4f60"
                            }
                        ]
                    },
                    "pa-IN": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 40834371,
                                "from": "*",
                                "hashValue": "62018294965bacd8ee8e9655605bca4540012c9d29f5337081c037db4a5f8da9c3ffa46311b8aae6a985623a71ce19d2bb4b9db9415418076c686b4c221961f1"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 77717,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "9af327ee2df2ae4f2e9b7f072c77ec5ee038ac0b7af7510df68648c224cf0e995281b7a16f5b01c4013bb57f490806dab6e61408c6659327b9066c91f9e3a949"
                            },
                            {
                                "filesize": 73810,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "22b62dde183a8b94f3acb2a29b021a5b519ca55c9d3299e57142e168010384d95ea5699a10fe759db2b888c217ccf02b85850461cb2eff36ea2a66b09d582257"
                            },
                            {
                                "filesize": 80397,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "49271688477f6a902f0422abaed36f2bfbf822dbeac5709da2e914e315cbe70e17a9503bfe1984fd561487814dfc93155a50207627cb722bfaf58ca3bad929d6"
                            }
                        ]
                    },
                    "pl": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 41743797,
                                "from": "*",
                                "hashValue": "ee74d96d9c72065ff1885b2f936992b3c30b34864fd814f082cbc4c98695212c188afc5d12f09fde228f2cacf6d9155ccc48d26fbcd40eb8feaa0168221fe896"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 77409,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "a94368a83b79eed13c6ef3989a5f092365ead235a2198b30016fa5da1ae0ec5ae76d7bd02cd756d5ec46b50e061372b0eed98a368637d5056ee8e86cf1b5924a"
                            },
                            {
                                "filesize": 75174,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "a94851e397bbabb3d2c56a70411d56af970bf75d8a71a1efbec86a72abb6007ceb6fdd58fba124ed452f21e57d0a586cac8f916fbd377b61f628f621043b5677"
                            },
                            {
                                "filesize": 80489,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "25ca214951e6e4e04689880c01ba8ef682cf996409e152367391bd312a73bdfaf2a88dc747c44f780ba95b98fff68d55f680f76e91f4341289be0cee6a6bcaf6"
                            }
                        ]
                    },
                    "pt-BR": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 40978703,
                                "from": "*",
                                "hashValue": "aa2f58c9e09b9af2339afa91ba567631e3faef370b16364ff42415e7300d0c046f95583ef4d2f3abe96cdc53dfd582b0d6b6149590d9cce8bca47ff26f76d31d"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 78081,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "7a51f4611ff48757f8472ae2f5bd6b9b211e9cf5761b8e896cf815435f7c2c8999118d5b36d0e07aa9bae662732d5367baf8bfcd5ffe445961d7e8529dbdf24e"
                            },
                            {
                                "filesize": 77834,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "f54d1ae35b8caf759f056873ba96f6e7d6a7bcea902e9538c6ac49b632e9eadd25a1b3eac4d4edbffb24c5917760a7bac3b1d0115c6f31013b1e88e89cf1e420"
                            },
                            {
                                "filesize": 80793,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "466d77e0c1712e3201ef7c87870da5d1a3ec151db87262e2571e962b693cbb70ee760e4cedc0f2a7f3de7507e1aa086538ee8d24e8c6d835bf72ba3d770418a1"
                            }
                        ]
                    },
                    "pt-PT": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 41005943,
                                "from": "*",
                                "hashValue": "3d525b4b3d1fe51dbb6d4b70a89b1eaaf346f530ec558e5985940f5d3bb34a92ec5a6632f8894ce5836d0d4cd907587b7e25ff8fb4b59aa807877b689b173e29"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 77937,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "33ad8f4400bbbe32aa8bb0743b83e37da70157ff1a7d487f02883fd98c69767ccd769dccbd676ebbac2702b98112b7058dcc8ee56b5eff310c268d1df0d38799"
                            },
                            {
                                "filesize": 75346,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "143222db7d6f2393bcf63e8f93e9efd428de7019c7f9e33287caa787181e228d1ac7591b1878ebc28ebf5966138b6ea842b5091d57092544f90f43f9572dbac4"
                            },
                            {
                                "filesize": 80621,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "78d9ceb0f700ee32753e88ce91e538be1f6762922d28cf10fe7f48f915ced9acccf8604b5409d550f50a452ba67ec6ff8d73e3e61848e42e2b6535461bd7a85b"
                            }
                        ]
                    },
                    "rm": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 41011197,
                                "from": "*",
                                "hashValue": "af0584bf1d33a6f59929e3ecf56c9b7e346b6157ee68237a9c9f11797e172510055ab53a0f441d2b5fdfcb5dd94b76c64674535cb5755cd95c7d6c7dd9c7405d"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 77465,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "08ca6fe97fbe3c8308926fa51ad70b8d65c2cf55e060c3fe5debd19dbb8a587804fe690e85fee68e2cc917c0db082e9d18b646b015f67561e211db9bd519337f"
                            },
                            {
                                "filesize": 70350,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "75f7feaad7aa6cb1c1e83501720eb472c3bb370e17b81a100b667b55a804cbf9deb4b608195eb4cb6f5bf42d5196fbabb237854574954cabed29d4a8452bba59"
                            },
                            {
                                "filesize": 80649,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "72963fbeb6e8fc7d63cbe01824e455aaede4ba9fe2463c0b156fdd71911640147a74cd540ccb51fe8c1b35b047f149a5bdcd65bf64ce0b6fcf7bcecec0aec073"
                            }
                        ]
                    },
                    "ro": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 41314273,
                                "from": "*",
                                "hashValue": "d5594ebcbf38dca9e87ca47c56a0383d78d07f4c8cc41d8da926f3af4a5f116281e24dceba5c869f39f54cc67e310e323f3c4c53511f5e8e96afc69902c0a6e2"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 77709,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "8519c852a18d5ffd54efd8f729d32a07c107ee43150d71d3dcbbd467f68b36dc6affd043418f9a502947d43f4954b06ff59fd354cea657779858fc8e0524e811"
                            },
                            {
                                "filesize": 74746,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "74b1b4d14d27e2078098ec938c558473dbae550c1bd715d0aacac76f142ce8a7ddf4cbd2324e172cf36e73b08ad5dbb6ce5acd0e6a7c4ba6ff518cb2e5897744"
                            },
                            {
                                "filesize": 80553,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "f3def7e07efca833f277266456c01786a789f9579de10af1fb4cc739a372a7705426ebe1517992cb6e6cf40ce189f18113ca4526b052ece611391e7aaa4e57d4"
                            }
                        ]
                    },
                    "ru": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 41266985,
                                "from": "*",
                                "hashValue": "44c132688e204ae7b0e8bc874371b30572d8cfa4fc7b392631255bfcb68fb4112d35cef7bbff077c6336bf50ba5d23fa4a7c0784291040b65164d6222065a24b"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 81129,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "166fc919151b7f93cb0b77dd5eb0e0a36bb095a58b93fca02fd120b535be21b3ffe1d78316f4cd4091a85461d418177cafd408f39e3e2071c2d05940e9c5fc5d"
                            },
                            {
                                "filesize": 80090,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "a762ecbb7d1b967f0b6ba81b8c29d89fb76d990eda965ea5f248b2603fd9c83fbe4dfc92db10289eb8bc705f0412b280a8ba70bc3d720fd4a91459c2fabc7b7d"
                            },
                            {
                                "filesize": 83361,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "c8ff0e49cd9ddfa48a5fbaf85534430b7a91e95b83a77b94397d50533df08d56c58d146108706817d4e91303bf6e082267b5fbec93e1ae78592828a7542cd339"
                            }
                        ]
                    },
                    "si": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 40835935,
                                "from": "*",
                                "hashValue": "84a7cf9cd3bfbd83728893513e101d1022bb94d5f42434648dc2f5c43f18c9df07a2fd91ae7b67e7680b9846b4408557b3d4e3548c035598349d45b8fefc22ed"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 73086,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "372ad8c046bdb6dc74019f8a1beda37215b99bc8345ecc036e519f7bf3ed7e4d113f0388b48726776aa33ec7d21595a374403acba35a26901d52f08239c66f7e"
                            },
                            {
                                "filesize": 80761,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "742edfcee3435fe496a2c7693413e724edf6c95513b1ab55351b43fe5894dd2bd53477b292e16aedfd76d4269388744524f38e5bf451fbfc6ce166ee40889df8"
                            },
                            {
                                "filesize": 77573,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "9c64b4b41bce8373b7ea9b8db0aa8018bf3f3a6a6bdfd8778f002d27c2fa969aefb1f344817755b018b848ee6db13157f26e30f93d56be91a0c77bfc639c0fa6"
                            }
                        ]
                    },
                    "sk": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 41521937,
                                "from": "*",
                                "hashValue": "e1e7c483907490d93563a13cc13810b8446bee3386894453df0cce5f040120fe5ce4baaa37ff4e0fbaf9d000ed0e382b15462e3932740235db6471fbecd7432a"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 74922,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "0f30fc441ef0277fd1d4a295087675ea65403004344a165ac2c7c460909a7c1e829b6af25fcd1169dc8051a4de7617d4484577f63c5b7adb26b5c9017a1fe9aa"
                            },
                            {
                                "filesize": 81169,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "ec7db46404cc50973b2249c46e36d782e44625f6e571bb109a7fbc5fc60158071fb01298ae0bafc052055bab5f7c678dfb2292c478d221deafd184d719116801"
                            },
                            {
                                "filesize": 78125,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "3f81e92d6716fb2766bf9112b67b490ae5948845d39132f79c515b31fa18c85f9d9a3d3a4aeec12eb19056396b284879d84d683d8389306f3d9dbc1150f225b3"
                            }
                        ]
                    },
                    "sl": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 40830615,
                                "from": "*",
                                "hashValue": "843ad15202a68f1731ae3d04589eb12d76e12c778ad53ea44e1f05ee56700364d29bc8e507b4e660a8c71e2cec4c818096586b76e7bc06cc362b26647dfad571"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 74978,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "f47385839bf0a2278a8eb9994c475722b21cacbdecbc8af93f015d25a3c4aad7599c73a9a560e3067950705b5e36fd701af42b50c172aac80372fbb8f9f57b5e"
                            },
                            {
                                "filesize": 80641,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "9dd5e138941b3c416989b18ca155dde2a47b19053bb032c6f2e70533b8954535c8403dded0761349e159dc1e176a0f8a7b7d0e3508354f15ad145374865eea36"
                            },
                            {
                                "filesize": 77705,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "50d17ab2cb0f6717c6dac8d244fe211417bab55ede89910b63aa79b1b5b8d0d50b7c9d6e1c9689c5993dfba543509da4e9d4d9b11d133073b3f232c8b289e6fe"
                            }
                        ]
                    },
                    "son": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 40823216,
                                "from": "*",
                                "hashValue": "6b91ecbf75cd4b1ff5d3365e49fb5790a5487fe236d1034dcdfe9ba2be10b1e4098df93801c75726166aa7ce950f45c8b81c5465330f8927a1d8f415d5aca111"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 78806,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "92d785fbf15d71aebfb8c297ca7393e90378c8b611d2443d4888c1af7f2447dd6f542238e16fabdcbd2a85531f6c4913617fdc51193a11f31cb25d9a6f9efa39"
                            },
                            {
                                "filesize": 81005,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "fa88f0708405520a69d834fbe11fb661a1fd4b3ea6463ad1e54c33b224f9e11a2b49f5aa082fb7b69eb37df8fa4c1b4e247b2b6466e6aecbb018d881c69322bd"
                            },
                            {
                                "filesize": 77949,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "da56177671e8391caeb49c7b71d98b8df1865d108866bedc92059809d03e9b25ca72784d0e4cfe2a8a9546992fed1738235b106a663d8a9abdacbbd8fd7091ed"
                            }
                        ]
                    },
                    "sq": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 40837235,
                                "from": "*",
                                "hashValue": "f0b8327310298ebcc16cd2369e478943dd11198043bb68bfd215e0d0c01856f37df609331ea247cef931052d0f3422a56cf8acdb50574d2439fd38239b7eba09"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 76302,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "3b79eae5a8dbb60e6872d9d3c786d0d7ea3a364888a074dad2b48869f33631d35258f562d0fb17f59ac9a5cd0422f405b2fc132a5dcfb84b5f464d483198f359"
                            },
                            {
                                "filesize": 80401,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "c331212fcc2bbbfcae5b1ef581f2da3572f8760daa51095f2bab46c16662f63fce259d9378956e4b10de5c268188988d23b6581449aac538d15e377db600b7aa"
                            },
                            {
                                "filesize": 78053,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "2f75a8079bef13bb97b773a61e0ca413079b42471d32a0760f2cbaf9bd07e62660ec6058239ec0f6700ce1ad0209ab2677ae40f7771ca7681a94af5cbe4c148c"
                            }
                        ]
                    },
                    "sr": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 41958989,
                                "from": "*",
                                "hashValue": "f7b890f4dd96d596a69e95d79b95034928d29c0e744d1ade50f55dc8acc16ebb9fd6006f5cdbbb4af4c93527039dd002edc3d640d41d72bbb65b7b0dfa124f33"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 79270,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "34d8b9d71e8cfbee0cf5d9cb62cf8cc8400306f38e235137223318c41ad90b382bae96f997141f200a6fd69c65608a253992c02746db6c88c4550385460d4c97"
                            },
                            {
                                "filesize": 80761,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "630a18657716360d98bc86ddbc7ac9f72f37f70db3e60cb6abdca1b21ee0a1e05290addcf3c1e38ac062b547cfecc2a3e8af1b4707efc6bb42a540709275b65d"
                            },
                            {
                                "filesize": 77941,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "515e005e29099bcd17da4104eb0955c969deacc8f436aa0b392b49f8d9a7a68a5b5b04ff00a1802512cf8124384e2f0ebcb170e2ef0d497127d7a3c7a5dba13f"
                            }
                        ]
                    },
                    "sv-SE": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 41368997,
                                "from": "*",
                                "hashValue": "fc4acfdff4202fa0d769ab6f1ca3ec72ab52e35abbb7f3367def67009aa52c158cf31ab920fb7ba886d991b78ea1a2eee7a20a084fabed584f1b4a7fd5c4b54f"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 73194,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "5662c1d170b87b3c27fa9018dbb0ecf6118ccd6020c913d3e4f2cff4f899bed729f98fa4ab536e38d06e5b0fd862e077f85b7250cd7063f45fb5379d73fa4fb2"
                            },
                            {
                                "filesize": 80537,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "7dd500bdbf8fd4f705eb61483b58970d2aa1f59d8f3bf225c6517e58da30712a4adbe32d85df53c40541442bd61d083580b792871a2626f09b89040c67f5dd00"
                            },
                            {
                                "filesize": 77693,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "2ac152ba2d7b68305d7052e92bb2a3e49d9c0c179a95c5a7689769970d86c6b8faf35cf56be0dbdc9eb202111b75b452e4690a25acad1f918a6e951a00234076"
                            }
                        ]
                    },
                    "ta": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 41046291,
                                "from": "*",
                                "hashValue": "750312b2080b02717e10d1208f0a593b93b4a81b22db93f961aa4ec9d145c3255c6672428881495db7267b81655168a3b00985f22bd00ac330a7b28e31f40ee2"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 72918,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "ccba174317e606d48090f3ff8f405e8ec5f6654b715d66c58337f4dfeef4705fb7461d24d36078aa1a647b841c69181de6ea978f16fde3abfbea5dea57cd679c"
                            },
                            {
                                "filesize": 80849,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "a1c404e661b85ad38e9badcdb116b26cd44b996c54f757822497d2f4f47bbf14ac5391bd00ae0a46f12bbcdc2fcaf8dfde68b285b2344a4dac01e7970dab788d"
                            },
                            {
                                "filesize": 78369,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "379990a7a3b2c9c9ea2809282f0793522a4eaf2c5de083c6a2489da2cf677567f4b78a783463480c0bac1cb1c9d70bcc3930bafc77b3852fa4d9613254a1f87b"
                            }
                        ]
                    },
                    "te": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 40852035,
                                "from": "*",
                                "hashValue": "fef8c5ca5d522b5054c8b2d55cf313caa20447637906cd28dae7ddd45fa0223f0a68b39af5f5c5ddf11cc7fc360068ecb18e98e77b38d0a2c5563d949ca79090"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 69822,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "dcee88d8bc74b4ceda835c0ab80d2fdaf4d099b2eacaff6937f8733e8a587927608ec8becdc1e12c77f98bd0a60e27e753224c30dbf186f067c3465e57bfcc14"
                            },
                            {
                                "filesize": 80853,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "8f65adaae42ef2ea4ae4f07f2e4705960ec46d1355d69980a10f106d469a8ef663cc3aad90dd05a2119099aa73f07612f76c91429884a35d21b5910c82941438"
                            },
                            {
                                "filesize": 77833,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "14fec0f638007740acfe73d6a9045d64f03f9d3cb1571f4b2eaf7eb31d8f1ef48cc97381be74fc93bdc966ab9c9934c2e0f88f29ca0f01990084d719c0f1fcd3"
                            }
                        ]
                    },
                    "th": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 40831787,
                                "from": "*",
                                "hashValue": "96f5a5546949e07e1d0d8b58102a3b57160079706340432fcc9336aa77fdc622447081126c2ab6f51456159f8e8236821d771bdcb4bb507120454b4ed7a4ddb8"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 75830,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "3920e9d77768f976e1f912202a5825b5cd46d5339cb5420761a136fe487dbf05bbad616b7c3dd4796aa6229a2616530b287adfe3339dc95124320bd95992b343"
                            },
                            {
                                "filesize": 80701,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "389d233a6a8a0ba75f2ac7b3c9a605166772e91d7918c3f1c2d2771fa1a077239d8547aa329c81a0c3095c417dd7e4e7b6e607059a54ebfaa17d4c23436387bf"
                            },
                            {
                                "filesize": 78145,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "49cc0fe2eeb4c9a6ced22706a616fc5c74e6c1ea7e984a94d1f32100ba8590b7924ef117f52bc67b7ef43c73ad0ca1a80bb60daf76e800e36505f9caac3b17e9"
                            }
                        ]
                    },
                    "tr": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 40828263,
                                "from": "*",
                                "hashValue": "a81320c173bacf8010b99eb8b00d4bb72424ad5bd1850cd69f7e21337e0e10998ee2e44961c891ddead314c986f721d8ca8beb0f1cc904bb94e6d47b5aef4b5f"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 75334,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "079a6ad235feee85e5ad698c5a82880f9e4db87c982375a396902100d60f32401b1a7e9559a05377a03639c452a0b8a0dd18fe03ecf77dbf20a6558c7199c50a"
                            },
                            {
                                "filesize": 80465,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "ef11d014ce590473d700e9d31b496fb1f1b362204f409d4197e27941ac183ea4672ebd550a1bfd1fedbf77ec33e54f62ce6c6494f2f382d81580c03bde656cfa"
                            },
                            {
                                "filesize": 77157,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "8d497fec609c8594c9782800f19ac8719d31e86e7a3ee2398694b1e120b96b0c3263246d1e4c1263be200729c0334ce979024c24767a0cefcb860cf0cfca57ce"
                            }
                        ]
                    },
                    "uk": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 41718217,
                                "from": "*",
                                "hashValue": "f7d6c4813ec84680836b87d06ced82312d585aa004af0e4a520719ae328f03b7efad7168225b3b6001eabc0de748f0b066b58a5b900c8f251a1c2c30bb975f6a"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 72946,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "315cbc0e978344b6fe358d808dd9f497c165609dc99d60f43c12ff4c5c114195c4fc02ee95b7e6d8742f36187131108919cbfc7125fc02b030d7db82c7cc99fe"
                            },
                            {
                                "filesize": 80397,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "c8ad7a9c26d15657f17768e46db2d995d60259f2a3f929fcfc49b35471216609cf5c5a999caa28e1493754f82f1b46beba24986485dd8aaed6bee0d62f8323b8"
                            },
                            {
                                "filesize": 77841,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "fc07fdfe3d78855980550ed80d3dce376f2311c937742ed3e01834eaa2f2af7188052c166c86b1cb26d22144abfc4e4bb7734ce0715f265638d04d58eec50fce"
                            }
                        ]
                    },
                    "ur": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 40843507,
                                "from": "*",
                                "hashValue": "a529536ec218e0e52f96496f9b4fd82cc9a2b163ee2dc5b447ca5b18b61153e79d6026661c9816eda9ca986c34fac0dddd15056f3bb248ce28e232d89148482b"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 69394,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "febdd910a5b081efce257ec544382450b00fd346e13d1cd472051f6c90e3cb5728b33571285ae45a2de23fc983bdd355ed13edb1de12792ca7bfacf2a098573c"
                            },
                            {
                                "filesize": 80625,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "954fb9091c7f9a93f100305ebdf62884f9901bb91c1c4a5116e7c54d8b041b9f7ec99576e99781df44dd472c6c3d81edaa03b4ca87385863e966f7eb5c2c9a9c"
                            },
                            {
                                "filesize": 77925,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "344ab21b807cddd04ffd83e67d5850dcde154df0b8867438e10792c0e28f577726a4b44a3a182c88c4aec7723eb91b4ddb0e57636d93e3aadb5854588286fb3f"
                            }
                        ]
                    },
                    "uz": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 40830427,
                                "from": "*",
                                "hashValue": "5094d48a274adb383fb8789f4c3dddb0de01e1ca30f0421d292d9085270897fdee8a1b781d07a08e5b28218591653620505661d75a98e4b9a170447ef9796eee"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 76286,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "f5407813dafd93e622fb8b0f29d9714d54bcc49f9f793845fd59d91fe10b5a5d123f595a6943bd70425285dde9d319a053c967242c1e56ae67c94e432ec3afff"
                            },
                            {
                                "filesize": 80861,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "8c4555c915280217f1b38e4f88f1bcbcb23fa4b9776e95f3f058203d9cf01fd955149274d8c0e33ab2d179e1a8dfd19c7a739c373ca4fe47bf4414e1196950a4"
                            },
                            {
                                "filesize": 77557,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "38b5b4a90d48f931b04b1f0e581c57013c0c8a0d92b7b72771d106b3e743fc49b4f5de4d613cf6fa3a2a5af9b984cf5c2d2bada386a327b31d91f9ab2bf09b37"
                            }
                        ]
                    },
                    "vi": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 40844703,
                                "from": "*",
                                "hashValue": "653e18589fb7fdd2e495ab06fcf78eb5199abd4d05232139bde56b11cc7fa7bf797ea2ce6d6a0e8b249a592210bb4856964a97c29d0478154d08f997eaf8d3db"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 71546,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "effabfebc55255ff10dd6d598b58f4ab89a3a660432a9aac1ebc74cabbeb91a633716c46df8d04be4512f19e4a5350f77346e3a1f183aae1e62652b3bfa1cfe2"
                            },
                            {
                                "filesize": 81113,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "e4b6b8fbd4c2ab715da7f06df3f3973430ff78049dcc63c3d2a0d5441bc00cc2c2279ea4b4f0559679fbbe60d6d2aef841ba5358ce97cc2c726778794849ca6d"
                            },
                            {
                                "filesize": 77777,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "cf5de52daca93270989934125d6f88d0919177a381e5bc8aecfd0c52330f2c94e9a1eaa25b7f63ccdc78ded6ff3e17907af23b099eed332089d23e8514dbcbd7"
                            }
                        ]
                    },
                    "xh": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 40836695,
                                "from": "*",
                                "hashValue": "dadbc172c59351342b1f82052df06b87308eae658342da8260ec2cc61bae49545aa61b49850e464b66d8e962346bd5da00753dc9eeca3bb4097bc8baff86a344"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 74378,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "959a47a0e8d33fc17a0e8d6aa863fc03d0b4dcf196fd014a2fcd0422668c8894ae933ae6e8e897d6b7b9eb46216a96da74c18e6ed1afae07f9b570e5c7cfcadd"
                            },
                            {
                                "filesize": 80513,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "ee5fbb98d48196914f635005691af9f135bfceb9eb2a654396aa83b97fbb2bed02ff73f93860685b00ebc898ad959ee8b8798ef68d8453872fcb6c3dc963f9ec"
                            },
                            {
                                "filesize": 77305,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "a1993d0d2cd1bdcada486d21d3063617f6970c823147da9c1cadfe2e2baffbaf3e98cabdb628405de1899707e4f8497f46e2c95d6ac9701022be80c5fed6baa5"
                            }
                        ]
                    },
                    "zh-CN": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 40827519,
                                "from": "*",
                                "hashValue": "3b8dd5f065411ff5fb736ddae26161b08675b205275eb6578101f2146e8ebe654f08b7b0e799117178ef126aaa5534c5a01125f881cd45b39ec127f1c86a0049"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 79030,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "62de84d0e42cc8be33ecc2e541a143ffc33a805a05931171443e7eb7d5cefd1cbfdc829120ef12d26497559dea947f82dc2d7ccf6cfd374631c2a91fa4589179"
                            },
                            {
                                "filesize": 80221,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "ba5961dccf3e3f1dd51a9599f4191df9d66d067fa816444b1c2ab7b391bdacdb10ae5a62858df3bede34ab9c3d5e6ffe79a7f72bb15845bac988ad793fa5b3af"
                            },
                            {
                                "filesize": 77405,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "7ae27a73d8ce50a18d812f7a7d7e9ea4ee223ee8aaf9f6c6fa58c3ddae2f8b0c92390db685276d80b70e16be0f0fb39c02e41786f0d1367026b4ecfec489c06b"
                            }
                        ]
                    },
                    "zh-TW": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 41001850,
                                "from": "*",
                                "hashValue": "00194683d173e384c07eca37250b324bb490c154f6900bd017e5bdf03e3e3dd4921ab4fb347b0f73c3511347f281621e55fa7c2ffad58f27f581e1ad42e931c7"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 78718,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "6b1f1ef6bef7391476a2f882f9cde13657b3358299a494aedde8e3e6e938a7d1026488d6827a65d381144f1fcb1ea022c626a4615c12e0316210ef69d26e8143"
                            },
                            {
                                "filesize": 81573,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "83802983fee8f9eb83e91e23ab486ddae38788aeab19971edf455e3c224e8311508ceda7879d2948c6957b916648f179d58ec33d8970a84a1366f89a49354cd1"
                            },
                            {
                                "filesize": 78389,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "a7d93488e1a244ceab5b0eef0e9815b11e4ec5f95a70d23962f6bf069f88fbb2d87c9ad6e350f95ab6b776ecbc8555be30fc7bf7172252235bdc8404f9c82b80"
                            }
                        ]
                    }
                }
            },
            "Linux_x86-gcc3": {
                "OS_BOUNCER": "linux",
                "OS_FTP": "linux-i686",
                "locales": {
                    "ach": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 44881756,
                                "from": "*",
                                "hashValue": "fc643d792d30cc4961542c68b17ccf0560411f8e5d926b6470c01785ee0bf723d957eebf4a093a987a579b807f351ad570003d52019147640e6b4795a9ea1c28"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 4805557,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "a5e6ee510d672212ac51bc76e6ded308b26e8b787e19a6c6d84f4f0812445c7245cf12869446c2e6ab31edba35f1ec46d7802c7ed046f40dfd83c8683a0d005b"
                            },
                            {
                                "filesize": 6673529,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "74cb8d942a3cb87dae0172abba0a685ad7f035b48a9401dfde91d86bd50a597b4195185a70efd389f98b5bec1977dd066b23078d90994d73bd7644e025f3dcbe"
                            },
                            {
                                "filesize": 6354262,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "459762f112022ef3bb58390ef46b0fc45592a3dbf5eb65e6fc6d564ba079163d45ccfbf975ff8447e16e77f4a1adc165ec291e41806503f8b3c66461e6e62342"
                            }
                        ]
                    },
                    "af": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 44882496,
                                "from": "*",
                                "hashValue": "725556f4e6412a2244f8861c1d3b0031ac6b60357a86365b12b7c76960f596045190af97c723f4639556dbc37501d7a043a9c9433218ab33404f1cc869713323"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 4805581,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "6f8e13f4fbb61981892cc6134c094f12b1db960552aa5f95d99ace0286922d1a725d3d3c7c6f1b81182d9cdb8e6b2f888f92ad98e4a5eaf051c9b445ec13642a"
                            },
                            {
                                "filesize": 6673557,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "f4eafc833992ca296a41444c821acc21a64f59c030c668f212d92c8c769612df8fb8b4e0f8685b64d128775c89e4d31d1e4f244f8cf5917bf1eee05a353ae790"
                            },
                            {
                                "filesize": 6354278,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "618ba691016513ace6bd04146fa64cf78e0490fca4f7c2fbd857782d8a9ff9e619c0a47d0ad1cd05a6fe417f0f3f4adccf2df26392acb537c3418e11fd87ae59"
                            }
                        ]
                    },
                    "an": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 44895044,
                                "from": "*",
                                "hashValue": "8a246e8df54834e51b88effdd8940c00a9991a55b2f3e23a6919463fb954690e67a054acceec255a8bc49ffacbd5da45e55c9cf46f8f17c2f37b7584d706ce9f"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 4805589,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "553cfdf033ba553cd360a4337e74bb723a9831e5fc65c1b30e7bfb41ed7b3669acfdf391b882e1d6a0d0a06691f6cc5bdcbe4323e4cee4a59ebeaf6707f91929"
                            },
                            {
                                "filesize": 6673549,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "66e161a6b1b1b069e4b70862260dee4254799122dcd2b19951261b64f94c40f60fa6484a6591d4aebd65c0218d4f4b83a7f676c117ae5396884600f7cc3e9748"
                            },
                            {
                                "filesize": 6354266,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "2beaad61d7d0c2b13aae41d6727039753d2cbc8d6a9d3b25d0c90dfdc928b8a0b55098d6e13558926c53706ff74dc321f15cdab659c89952f4b2ce878d860d59"
                            }
                        ]
                    },
                    "ar": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 44893796,
                                "from": "*",
                                "hashValue": "f69adc93fbf914fccfa5d1b6cde06c4bd2900ce1ebad145e3e79c9d2a7c71d51fdf401dafc3f13a57fc8c6f5e84ae44029d96c3b38be6ffceecab19572f63873"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 4805557,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "187733fef6079cc0e6e79f448f0bd662e7b89f52b93dbbe2eda6528083da2f7df5044524e6b4ec3224c4a99d566d2e6c031a65c4a40088ea6917af1071717ee2"
                            },
                            {
                                "filesize": 6673525,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "cc8e83105e6b5cdded71acc3281be9dc0df0b62548505109a6bcc4c2f6384db433a6aa475ad3c9da1c7ae52e3df9f5b6cbad8f2f9f7b3ab058c98aa424d77c1a"
                            },
                            {
                                "filesize": 6354258,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "6ebec5c245a4132bcfd4825ce807029652125bf49b640c0dac83211e576717c1181400abf38c5b8082b5bd7d9e8e93343cef8d56b8c54dd7cd6efb3c9cee8b60"
                            }
                        ]
                    },
                    "as": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 44893168,
                                "from": "*",
                                "hashValue": "7d65b491ca87e1f3c72dedb494d6a5ca01ad511bd6738096c0b666a1918964342b30ac00b2ad94adadcd0393550f06b04ef69e5c7ce1a8b199ee59416a4670e5"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 4805577,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "4315f031279b502e3633eb722c2584120cada85e3ec2a82449f6db2c8ad06b37f098782f3a286adac879c8334025d77f770b15836bc8004042e9de41ec1286ca"
                            },
                            {
                                "filesize": 6673557,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "8aa61486958f08287812698bcdb1ffad93cb3c323ac2066a432690395fe42f24ebfc9addb6c2b186820d5633669c6945a3b26c20643bc4d46656fbd35cf3c4f6"
                            },
                            {
                                "filesize": 6354306,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "a497f4e95a3e2db120aace72052f517b0e446931e019b457490bfec791d1a441bf0fd703839cd9ff4bb6c09e35d9989487ee821e6498069377fb64645b328ca2"
                            }
                        ]
                    },
                    "ast": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 44889916,
                                "from": "*",
                                "hashValue": "ab22cb5e032e6469439c20daa074e320900558afe977e12daa3ff559bb1359864e43fe96f0fe59079bd8a9bb74cc9128756694a74d0370202e08c5f99f4c16b5"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 4805581,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "53f15d3d670bcc828768dd8fe1008de15d55bfb94b81c7766c3f23432bcc43f94b9f05d79d54d41116f2de82e115281477f2d8d3666ee58ee8d7b1d2bafdc17c"
                            },
                            {
                                "filesize": 6673537,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "57a40fc174d57c05351667ca12e13069cff791f22de17f1d4c664241ad67b7f45de3e27e99068b63a761e79e9d1919d91c15af72d14729bb82df5ec40b401621"
                            },
                            {
                                "filesize": 6354270,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "5525cbc4497f43c0fd2752ab5c55fd7e0883e074f5194ce2ab0e8b1b6ac77c33f5e35b77495503d8b8cb08bdb2c2fd28741d88610cfc0e642ba81840813a69cf"
                            }
                        ]
                    },
                    "az": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 44889584,
                                "from": "*",
                                "hashValue": "f8ce1f0be8f585cd1f9854096b0801595f74d608ac5fcb9f1860c9f3c204ae842f9c687aac9dff7005335f9b40c526caf2e0591ce8f4f052b745a3187849e250"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 4805581,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "6f7c940bc302897ed7ceb2bbd8eb4a83eb9c4a65076ec49d1a2e0a62dfce39069235dbe649fb7d98b99206ca900f69cadbe603674025a66f3a1f01e48292fddf"
                            },
                            {
                                "filesize": 6673549,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "273d5926977000e915051d99995189e4a41d62ac83a7222e5ce262542e52f4b2629375624d3898f2778054d78d8d3f48b4c3dd7856a4a776fe9cd6a9e2478622"
                            },
                            {
                                "filesize": 6354258,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "d373824fa37960545969580d10835a50c88cc65113c2f7157dfdd470870a73e29f1ac35524b047440e7288dce624f25561e98bb7976bd6f1a5d1dab7f7253db3"
                            }
                        ]
                    },
                    "be": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 44905000,
                                "from": "*",
                                "hashValue": "841cc27dc53b2082f998997845765a37553ee6abd7c25077e69af92356db299b573c8210aad21b55e391637bd6012cf583d3ff101786121eea2379a8b40fd1fd"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 4805617,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "52758f9dc000c1df1104a2cefc054e9e5ab6fca3c3b19d57ae4640363f2575c9c8d8989078d72dacf23a2a91e311885c91112c3f74176ffb887232621b12025a"
                            },
                            {
                                "filesize": 6673573,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "a3d3f104514d227b9df0f0e62fd65e2c6ddb2794a94b9f0abd623ae90877028d40a130d199a5978151697da993bb3f0a1a823b8750a2497ba3eaed0d826a572d"
                            },
                            {
                                "filesize": 6354294,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "785ae3a5fcfd62d2ffb48c4c57aaf2176d570becafe57f204048ce694fc86b3515672bbb7499b86ccdb76950b6419377a0c9a2f18ebfd9544eab1a5e76cf86fc"
                            }
                        ]
                    },
                    "bg": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 45580152,
                                "from": "*",
                                "hashValue": "2d0a294f1ed9f55d39cc357df1ff051fdc13e22f29f8b5f9a11585c19c6c84f98ef154c9696ab5660da2a07c730d0f8e4c090254e21877cb89c3762fe5615ef4"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 4805633,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "a71b9df205721514932ddafb296180605349ade12622b61b5554559574fa6bb3ed5b03a7991a88d33f99b3de74c5c5095ab5ad3aaa8b283a5bc04d1344c026c8"
                            },
                            {
                                "filesize": 6673605,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "59f50d4c6b07dc67facbf67e56cf12730562711aa50c149ff41f00ec5e5b3088545af6136a44761035adfc344d9be2109196eb049dfbaada341ff5e18cfe5b2b"
                            },
                            {
                                "filesize": 6354334,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "3e3aa9b97e1a7761d33ab327571362cfe9fd3a045045b28ce294bf675b2425764045b7a02b3cd358fc059fd6224c099cd091ba7b20987e0e3cda9bb1d9fefe6d"
                            }
                        ]
                    },
                    "bn-BD": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 44909044,
                                "from": "*",
                                "hashValue": "f1d1804d281d2ac6f130ef036023cf0b206e91626a2f49b9efd9ad6c64ee7d12ef71098bededea38c86b08c12d737d9e60697e4c423c76d50085255981270256"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 4805637,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "096171e1983c667abeb53beccbd44e16e0cc35f064acac14c81129a79ce666de9e66de73647044ff161ad5122c672f5b4fe62c9b00d712cb71422d6f2ec08156"
                            },
                            {
                                "filesize": 6673609,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "d28ad3a6058198c4044dd7c3407e232662412eea6da1c41a79447f400c3a6488b88738d4053e54adca91655346a3f94222363fd24146b4a4a317e3076fd8143b"
                            },
                            {
                                "filesize": 6354338,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "2ca624c3655639fcd5f3cc475a81e97b1dcdcdf23081fdf98dbdc4c946d5a141038c8ea1a8a58abba77961a9a9d4a4c41ee779e19b37f41edcb50988834a5196"
                            }
                        ]
                    },
                    "bn-IN": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 44903896,
                                "from": "*",
                                "hashValue": "1f3cb57c32dd70019378ed4275c789db79b307227b2a8f69a74d6a545d4bc8a100a6206aa36f9b88f35bd44fbc40d577a2599fdab24b68e9623c6cc0848403c2"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 6354318,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "643e4e0d1f2aa93a5ff28dcd86febdec1f06d52aac60c8dee21a49d0de7a94d0010b04726886ab5f2a3746ccfb54b712c525cee9c10e2705e6b465b4afe1d379"
                            },
                            {
                                "filesize": 4805645,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "18f63bbc888b1752d7f85d26db9cbaa4cc41d6dba81366d3273521bb175af810317d6fe9dce04e274cc034598f1a73aaef9fa14c17d3f876378684484fd53de0"
                            },
                            {
                                "filesize": 6673609,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "4d39244278f507736cb0919b4d0e18fc6970eeff8cbb0cefe26614ed0bcc6821b2c610f9e90b37b0d35c56873ed63323c53acc97aa698d1fe17d339086334c04"
                            }
                        ]
                    },
                    "br": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 45601536,
                                "from": "*",
                                "hashValue": "8e160003b817d8c0216e76d17702401adae88c370cd65068da65d2814f4143f05c173c2785b92978ede570e22b69348d84dec0238376c53e8f97a1fa2e653670"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 6354294,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "28e01572bc0d86d562abfb6d7bbfb0bf82b638a27c8cfde6a0d7d69312c3cf5ab51599c6590c047dd8dc298e809fde47e9824de0ad4953312fe477367c1b7ae1"
                            },
                            {
                                "filesize": 4805605,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "3ddc058f7e94532e4610059658692de6210142d28a7016d40aafa62258805a1ad710c49d3f71d026fc5ec4f689b0de040465c0dfff7c66dc2cb8d99d52e3db2a"
                            },
                            {
                                "filesize": 6673585,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "3c76ecfd361e0d31395287efeb05b12dcb7eb0af4731c4ab32d48a2e8bbf32efcbc1f38c98a73d5c249fba0551cb3baecf6dd7d27076b40774024d0f7a99f679"
                            }
                        ]
                    },
                    "bs": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 44895324,
                                "from": "*",
                                "hashValue": "ec35c424d7dc02c5e6eb2a128b253772b573f1554c6cb687ff67f65fae9b017b4d8d4ef8bc76dc2937ece9141c2023002514166f175e9fbd9258a4d7cd6ce042"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 6354258,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "ecca4076828bffdf9434d210a7eb625a224f2ace0facdf7b0ef8ee8611198b606c68c87d27fe7e32cb6fae0c34d0f4cca21bea57a36f64a47e18a0eaeea4faf8"
                            },
                            {
                                "filesize": 4805565,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "90b85772cf35bec0137bd9215c2a580ef0f3196ead5f879a53b07d9574416264839d65a9a3456f73bc8f012251ca1ac946bba5d9c1594a161982c5c384cf877b"
                            },
                            {
                                "filesize": 6673521,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "bd5a58d9850bd435b4dbd4171aa628df73a32606caa5c113dea9d4e037c8a37335ff8dc4b9b790feb27b6323f334bcfa6323bc1224624322c21d3737eaa260a1"
                            }
                        ]
                    },
                    "ca": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 45219288,
                                "from": "*",
                                "hashValue": "d69aef235d58f7bfdbb153281632b248e54ae3d4e151c1d33b064a4482638b16e4f3d4891aa65260d6012264e492cf2588e4d1231e75d802448610c9df07b95f"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 6354290,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "e448e58e17cb15588c76ab906f64674c9952cfb1343d720caf10cee2def2833c851615fc87c6897591966a144ede1f73bc77533607aeae757a86db9c0d2db0aa"
                            },
                            {
                                "filesize": 4805593,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "cf1d15f4f6dae44360221525646b5cf465d0d787d1e304ea1566e1d9406ed3511815833b316e8676ace245c20ab23651e971de86dcab8f15df11c3f0d9a8cae0"
                            },
                            {
                                "filesize": 6673565,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "6f3f795bba5b8b8cd77b576bf3c4681240bd8efc242853814f0e0342549743bbce65d40578d9a0c92fd067f3f062cda8abad5e92edd693bf7a35fb0627b6ec30"
                            }
                        ]
                    },
                    "cak": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 44897788,
                                "from": "*",
                                "hashValue": "d650da3b8a313357aa1d328358a2033c5aef1956d6fb6625ad4c311fcb68fb020e46768884d8eaa02f4320a107507c88c2e2d5ad5985aa820f35f25956135562"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 6354270,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "6b67044a82eb42d4efda188598b6105bec99add35a600a5a5a8ea307c7a6d876b38a11d4f049e22f275d58c8e6ec22d9359462fce3eafb0b3ae70fea65db71c5"
                            },
                            {
                                "filesize": 4805561,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "9f351a611ea7a1d91654072e3493ca8843d392eb13987c29b0680d49b5d039f7e4d3d1759eb8eec3197970a1d648763351790d32472b4ce336b06fb43e202494"
                            },
                            {
                                "filesize": 6673517,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "6795ece0e208b6c1b4da72474b2ec9100d75a8624ea678b27bb41c6e000c417936ea11ea8abaf802c8832c6cc43deb70adc205cc6727ed5513f1defaf97bdb57"
                            }
                        ]
                    },
                    "cs": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 44891500,
                                "from": "*",
                                "hashValue": "df80449a967d7d0529173a66af20ae7b2207d436c69dd99a84092d52e118478b62e362b9c2c2ed81808451ddd08d9a851e187d8a4530906241bb80a46865b508"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 6354266,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "79bc2ccc1e1dc9ab85023d5d7c1ea6627a4381ed08414b3d0730c03cbb69a2c748c7d65b7994e5a16edd2a236442a4ada006e4bb77f14163136fa3f9a1d84ff6"
                            },
                            {
                                "filesize": 4805577,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "784ba266be3e555cc9eeeb1203d1cf7ad0c8492d6daaa7771a83b9c6c01109c42614d4c0ea4a1bbc5c058aa1593d5baab89e3449db1669f0f1efcd357424a381"
                            },
                            {
                                "filesize": 6673549,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "c86f5465228fe6210f3ee7c4b95555c3d10ece2a3043f298c432f205375b68a6566226ddd5ae970875aba7dea76a7b62bfda2f75bdcbc687a27da1f04bc37cc6"
                            }
                        ]
                    },
                    "cy": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 44887820,
                                "from": "*",
                                "hashValue": "b3e7b1587920f7fed64b56e0a87022cf5b09b2b3aadf8b921ed1b17de5e58bc5064380d7b5110e7dd0631a48c85b35d66ecc78ea899b6149c0d77392b3eacf53"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 6354258,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "8d7a8a7d39fcdf46fe50360c0fc691609075d9b289a6c345efed5cb334ee2b3e4629252abb16b2a0c5fe16b26659fb9b19673daffe827a645c7cac2ca19c67b6"
                            },
                            {
                                "filesize": 4805561,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "90e0d5486dc53e88f09a8d8b6d97af47ad5f878d06126073a729eced953531fe9c34c740e197db69d5042b85be3852609ef9c9fe930b484e6a92f74d33ae80d6"
                            },
                            {
                                "filesize": 6673537,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "1be3dd0c8361a618d58339db1175560bc700563c24d548b8a8e40ec226e002ab5e7494c888bb41c59d4c55151ad27e8875d71c1e15e1d2457a3714c00c4e78ba"
                            }
                        ]
                    },
                    "da": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 45399472,
                                "from": "*",
                                "hashValue": "301618f28f2dbe32ee6baa7c5ee870d3b1d2fc313ab36e541837f30ba6555e84ad116fd32276363fd75576f9880fbac49270378ee9b64cb5538ec324eedcfcca"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 6354266,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "ccfe972ec0f97cee14443421c0c1a1f63f297e80c5ce9b7144444cc221150f651b5e03682dc2e0d51aa42b8d8990c881f426d6262de07ff9dce50c16980300ef"
                            },
                            {
                                "filesize": 4805601,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "65d038155d13999c8e65878e65a6b6d7004d801a190500984826f688900f3bd4692b4a57e83a684d5f0b48ff1ba5e585c9add55fd0934fc98c29c34fed3caee8"
                            },
                            {
                                "filesize": 6673561,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "d45e0a41ae08da471731c31a672dcaaaa67a97442a131ec8b52accc5f860b96fca7283006ec550b30aecfe2cbe21f0beec94638b1378785c66c867aaa88c0ad2"
                            }
                        ]
                    },
                    "de": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 44894424,
                                "from": "*",
                                "hashValue": "1cb3622ca87bffebdccfcebcbb16eab32aecbec52853e522f94fa296f63f11178bba8e8416b9f00bdfec6f8e2b38191591ca4a3ce5ec73c9bfd8ea3884f6ab8a"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 6354274,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "eade65a29d164202751c0886973e86aa463e3f109b06becf0d53ce721da8469ab88b5035faaa7e5124767235d92100933aa45ca05aa2232e650ce6a8bae6fb5b"
                            },
                            {
                                "filesize": 4805581,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "d1163a4c7b26c2952af639091048459159a6ce17dc45ab43979903a26bb0d115a5440b3df5f50628f136891e32dfc4f6c8226943ad87cb2bce784475c0317f50"
                            },
                            {
                                "filesize": 6673565,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "c4f98f12f91cb055c303cc2ee4f39aef54d2c2e5c3eba2a5cc5e221af8e94eaaa65a51853d81410bb85daf2c78d66511a1e884dbe706f9d13f871abc1f8a71a0"
                            }
                        ]
                    },
                    "dsb": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 44897628,
                                "from": "*",
                                "hashValue": "f75239a84d61dfaa2e5e97220d34eed6b527fa48c9d5905823cbc532122c7f5a2b8f7cd9f1c8f8ed84f9a8d4b48df8ccfaae5d4736229118a8aee1804018a9bf"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 6354266,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "983abfae905eb902e23099f2cc6c8fd7570e36c6c107682fd1f28848b8fc79c32b69c492bd197cdea7139bcfa2c28b8266bba788a147f6b19ee39ce46ad9ab1a"
                            },
                            {
                                "filesize": 4805585,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "b958c58619d282b41510ceeb2ff0d1412c255939617450448510f6e02868e5891e8a3cbebf87aac3f3e67484efd7b3e553077e7e88359ac4fefc1182b7fb26a3"
                            },
                            {
                                "filesize": 6673561,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "0bd2077fd3c2376c1a6e2d3fcadc00ad3b2ed251eb7a247322ef93a5dfda54a55a25de3fc051575a609b963b0450096ee10a5696cccfe0224c627a45cf1c2902"
                            }
                        ]
                    },
                    "el": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 44910272,
                                "from": "*",
                                "hashValue": "d97135478787791bd1423db314da7315df290f7e515c250c04041e2dc6a2c276e7a9099f84507c426874de286615a7ef81f06e352af8c809f9ff43bbbe0ea3ae"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 6673581,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "c802e4ccf4be8a0c74bd8e6c17660a3469f10e44507f16906fd1458f72a277f694c6dd80993dede9e1945d7e513d2e05df9a23ca754e4573da8abe59fb490dcb"
                            },
                            {
                                "filesize": 4805609,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "c32e0800db6fa2667e3310c9e22ed455aada61e41f78dc8f8f88b56c0d37a9c773d4f2ff4c992a5da5418b950f4f5490de4efe8e8497e32fb392d6202d0001a5"
                            },
                            {
                                "filesize": 6354318,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "2d7a93992550078ace4a853f13d31f281778df04ef419df8833dbe684692ceb0e056bef4853447d5d46cb8d0127dc02343c302c0420c3eed877e52fa0841b26c"
                            }
                        ]
                    },
                    "en-GB": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 44868592,
                                "from": "*",
                                "hashValue": "80b3a1c156475e4fc2fab5050cb755400a1df9bb1c1b04b685cb69ae057eb5cccac4dd4b639085f7e5bd97a7e8626e8da0b20915e651757ff2485b4c2de72228"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 6673633,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "e8749a79a35918cd1dc97e09542b36616b20ab8e26e3e0a0dab496bbf43f983f33e46bee71126830636e610c7a1dbb7d343286d6a69e2f2621e78ab19cb0a664"
                            },
                            {
                                "filesize": 4805673,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "0e90759e735a147b767bed700020c85597a11aae5813619d08a80ef0696ea6e331a246dc2515e81bc7219ec162429f946d13e7f422170a7e0482dc0561895d15"
                            },
                            {
                                "filesize": 6357834,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "033f352a5b44dfbaa14dcde6526e9ff336b914de3661037d478224f6f4c3f38e08fbc499810c4e18dc18a382daf31db507fde3ed02e0ecf1bc2499357b9c7b1c"
                            }
                        ]
                    },
                    "en-US": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 45032750,
                                "from": "*",
                                "hashValue": "35178cd290556b8f31b1aab2a2433019ce0d9e15bd552d621eee393b7b970e1ebd25beab32800d981ebafef7373a76f4d756739ace5067f5eb65d2dc07fc0c0a"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 6354298,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "5150a20bace9401662c6e5221a678acb8cdca2a67536a671289271d166ed27395e362c9c6b25afd05f0ededee95fa02295552b32c29f9e299a764eab02b8bf46"
                            },
                            {
                                "filesize": 6673609,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "b17b20c6ee3015fddc8724fa6604ee3a3fcfcb0f4c282702f76b77a7912b6288b7ed25ea117867222cefd1ad6d1e7fbb19058f50ac566acbf5e0d3808ce77838"
                            },
                            {
                                "filesize": 4805629,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "67c2d2ce9a54119b367c10f9fa267b0b1805f9aadd3852aaeeb54adfda6d046935db6b7b216926ecfcd107eedf2f1a443ea2a377cea4eebe08b6186d8b4b1038"
                            }
                        ]
                    },
                    "en-ZA": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 44867400,
                                "from": "*",
                                "hashValue": "fc75d2fd315b58a6269fc366f2c21bbe29870740da286679d350dbeb727078852f987fce03694c22f12a3216dae39570cce8cc8270206bd39c1808e85a4b3e67"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 6673533,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "e1e02759dafe77d685b2b60ae3b877ed1e1ab08daef4d40eae8f7fd76b151df9e672465731d3531380306d364d0f43a30711cc09a90e0a28034403c47a732aa9"
                            },
                            {
                                "filesize": 4805561,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "974c164d55bf004834a8083be50a44148f9ed939ac1e60de930036bdab63059b972eb35a6d7659d286fc556f69d4501d322080f8a45a89bfce10d2019622d7c1"
                            },
                            {
                                "filesize": 6354270,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "2fc39d7102bdb447fe1b65eb99856a42062acb1f1086b36d150ecb7c43c74f82b9c5b2ea4060a39dbedbf4d91a8e48c2bee1c9121a719c9bf5d702c7175284c7"
                            }
                        ]
                    },
                    "eo": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 44886828,
                                "from": "*",
                                "hashValue": "f87c8ec2d1f663ce67c134174dea21a7639abf26034b24840cff8c626738c89ccfab8f6da72f4e9fa0549e4a35d38661cdcf3bc22ba4d605d210bd155ece132c"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 6673545,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "056f3d2b20edea761de11c468ef4259c1a99fc7af2857a6e5b296066bfe853afcf8f5e45bb0e6e386244ce95f7ebabf6f67b690f2a398babe692e3991a84b88b"
                            },
                            {
                                "filesize": 4805569,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "87ac1001e1ea20f4068f91c980616298ae2474597c8b1ebf7aafb4044d05948bc9b32c9ecfd28e4229c204d76bc5e5b66485223651592bc5ad4783a611d97fdd"
                            },
                            {
                                "filesize": 6354258,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "7c1380f4a7e77630cf82c6139654cfba8450a4b1c0d403d2babca44363f6519c11874e0a7e9fd2f2803fdfe615b3a5fb6b0d3179733d7814ec3c750507f967bb"
                            }
                        ]
                    },
                    "es-AR": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 44892880,
                                "from": "*",
                                "hashValue": "0bdad47d51291f97ab1866e1808851f778b53d1d443bbe000fe6f5f5182fab59f0dbad0f3eec6d4e88b53da5226e522b5039bb81f4bcb6c372f700d4f410bf10"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 6673565,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "3a80bd457b67e0ca1c5cf730fa3e67d89c8a7ef4be907bec4d700305e3e6e85de35554b20048e64f01bb2c330086265ff36a3b24a39982b58492d235f5390031"
                            },
                            {
                                "filesize": 4805609,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "bcea98c1fdb792e1947de0b6206c93c1b97477713036eedbeb4249c529ec4f1bbdca847580994282d60adfe436338d98f93eaf398d7885fbc92df6736d50d9f7"
                            },
                            {
                                "filesize": 6354278,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "4171e57b67a104c3ba0c36f6c0b6c4133105f9a3f64842c853e6745c400ae8b7e225f43bc5fa28bf7d4637daddd7dcc2a87697fbd8a2151267ab0733acd7cad1"
                            }
                        ]
                    },
                    "es-CL": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 44894240,
                                "from": "*",
                                "hashValue": "8f431afcb39228d15845cb509f2c6fdcdb61f360edac4cb14b725e24ed77c5020588a890a5493fce0f809b1846deef2602a614b3db40bfbe7c3affba5c23e339"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 6673545,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "355e38db026b791fbe649430ba72bc692e0c6799a1835d38eebbcc09863ba3c5f303b3d1367a8e5122be0434764f4e1d3ea1261e01582cd7884320efba9f98c3"
                            },
                            {
                                "filesize": 4805581,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "3d27e248186c3cc2d4b23a25adde3c1231d3c47788a5d4590d8bcd846f5b0aef2c7b17b85ac5bbe1af6da5692b2e8fd7ec89002f85d9d0cfc7ae3328239a787d"
                            },
                            {
                                "filesize": 6354274,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "96875406c2b794428a439b2e1d75c6ca13eb6b4bed212598d28e107c3583cdb55b965d6a6569fd04ac5b800de8f76aa2161356b644ca54e09e618fadb4f69b55"
                            }
                        ]
                    },
                    "es-ES": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 44817076,
                                "from": "*",
                                "hashValue": "3b454a10e6b59b9c4d7bea7578a300cacc05bab3da0641b5928f33684107f6d4265d3eb349e7a87257f2a6d453df0e9f3189bb0f8c6ff7f5330b65e83beb7d75"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 6673505,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "65ab36f8fce550eef3426efd47349333ae387d8aeb1af48715b8c463111b9153508fab6871d28f33577c8ed97619a85600ed6cb5b2af7d65f1a8d5f5f2fb5b7b"
                            },
                            {
                                "filesize": 4805541,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "330f155f835f07a4123be8470394e4c68edf5599e9a006f9f756aae69ca30e84cee99e14166ab9a54db2115f2dd60307d25704ab37c6d62f371588beff21674b"
                            },
                            {
                                "filesize": 6354218,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "ebe8e162e8971e9f8744dde9f3f51cff45fe87ded74ec6804119b3f5dc808cf28e4d2c5a62c65a8d0ac6e261e5bc9172e1518f4d849ffdad30fc3c4cccdc53ca"
                            }
                        ]
                    },
                    "es-MX": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 44894976,
                                "from": "*",
                                "hashValue": "1bd322d228a4972ef156db76359f778cf2cf4f8afc251f4d1a97029239a03a0f2f9c98a7b85dda2dbc874834a56c04c853f50153299fbd6af7d718b4086cca5b"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 6673553,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "5b9c5ee6fc71aee30be015e0a5b8e60b551b7115c60c63e8c73a1b16770da13df9063c7cea6b5506568c076a7189af09ab2e879fa538a56b77378c942d6c6017"
                            },
                            {
                                "filesize": 4805589,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "1a4f129263972f024160cc6b2cdebf00cd20a7d4239ed11e8b69ecfdc3eac09b3fd27ec0654f10aff0f21d18a760265c94483c258d06924d7dd5bfcaeaf14c62"
                            },
                            {
                                "filesize": 6354270,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "d8ac348b8e1a4dcd09f3a7aee3484d50a013a90cf7019491c42118b881e91ce3c2d02c075083ddeda4b04a4274374a11d72bded2a02be4c88811ca15e67ca4fa"
                            }
                        ]
                    },
                    "et": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 45514992,
                                "from": "*",
                                "hashValue": "14c4a903310b1ad6eef72b90fc6ce358e90200fa17cd048fc30909246279ff01b44c5188a04580694e3d8239ebf400f9ceabf1fc8f35985fc54aa2cf2da5a126"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 6673537,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "dc30e9bd4f9bd80ca96df6bee0f2201d7be6a8ef10ecf88f44e56693bae0cecdc782c6c6c759218fe506c5aabdcd541c827bd7b9741097505919bc145432d7ad"
                            },
                            {
                                "filesize": 4805573,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "ffb08cc403b847defbf6a9a6395b5941428213b2d3314be1d3c7e0c734bd42902d60d5c9d1d43d70ee5bd2977518aab5c38e6af69cfb13838f63c27f70cf35b2"
                            },
                            {
                                "filesize": 6354282,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "2c6d496b2dad232485cbaf3370ca7cd2c751abf31c64cdbaacdbd01a32adcc42b26243e18df67eff72a73075d65b78cecfe65d87e7fee64d5dd5fc1667c182b0"
                            }
                        ]
                    },
                    "eu": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 44887844,
                                "from": "*",
                                "hashValue": "931df26e8f13cecca23a54fa244881a880fd8e856fef3be1fe474f563b003d676b7b15da14ac37e3dc528173a44a507851a3f75f7ba6f65b7e9ecda0677e4038"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 6673533,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "d2826987954e3df20e66c162795279758bc67f3ca757b390b4fec12163e826a157ad37b0e10277755adc4f2c6a6c36deb76f350eb551b9b59e581257699a817c"
                            },
                            {
                                "filesize": 4805557,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "a93b69b2cfce1ace9b1047304f9590edf5f6558be1cd714e53a475b763fa7a5553247e45b0934d7429a9a77d691e6551bae7a55e15c7a9d3fbb0e8c238dea021"
                            },
                            {
                                "filesize": 6354250,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "f90269dde291cd0baafda0c176f75c5961797a4671407166b668d2e737d1551d2c7691b5b94911859b73d45b7cc1662f04a9113bc8061f6ca38a949889de5c2a"
                            }
                        ]
                    },
                    "fa": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 44905044,
                                "from": "*",
                                "hashValue": "5521cc549515cabe10b4a659acc67a264212cf0a672eb2344ed93594a222464407663e91e1e6489b9f52f0a7858173e4f1b36944bceaa29668ddcae5e1ee43c5"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 6354298,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "9df331563449afd718bede0ab7a0379019dcc306287d8c246cfa0187eb5914bf3e291e9fcf1b37bf1aa6124b5028b3247b2a744616aeb4908dec1e66c87303f1"
                            },
                            {
                                "filesize": 6673557,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "6ce8f16c5a1ae336e4621c47035306fc544a0c1cf4a45214cfadba90dd6528e2e344341ad9e075113c3d6d20f6892d57f19e036093f2ecf040bd5327aa2624ea"
                            },
                            {
                                "filesize": 4805581,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "97c2a10b7400a0ff03953173b4ce5f7873dfec33009cc579d221acee8d775a023a3ae13b8b6d1e808f047667600f31fc7f6822f1747022ab069624bae471e7ed"
                            }
                        ]
                    },
                    "ff": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 44890080,
                                "from": "*",
                                "hashValue": "5becad9a7c087af6ee5c2dd56781deca9beb6cbebb47a0e1770e9ba3eb7d768dbe1b5cd86e4549302dc2d8ee36b50c4fdaceb34dc118dd345e4c8c5be190bcb9"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 6354250,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "4bd77ad5b96e7b7601d4ed35f43bb022cdcbc45475ac947be298a84a4a1a05fb68a48a3da82a3152f9fd8c5ff021396226612dad984944c93a5af0c3e966d36e"
                            },
                            {
                                "filesize": 6673537,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "3bbf76f2925de2ad1b7d823b870c2acbd08c500012a06ff53626fec9a8fa2031cb067f4a42fbdd17a06318e805a8619459d58eea93048b04fdc278f7ef6944d5"
                            },
                            {
                                "filesize": 4805569,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "9614de9c4345c7b447e216da953058bb0edf1dbb58aab9a0bd58c2f3d29e29114b8946a93fd2777106b2637c49a6ee98a7e14f92b7382212ef562d4052634f82"
                            }
                        ]
                    },
                    "fi": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 44884740,
                                "from": "*",
                                "hashValue": "88c5562d437f9f79ad13cd8be648cfee843c8c0f1ff23396d55bbb24e74b409be956c12af8341d6a732937fe068b42832398f78d169e73424339bd0f0ae4c27f"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 6354262,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "b9868f9b7c4f6e201576d8d8b14ff869f742618b6cccaa43a8b219bdeb9e7a142a2f4139c3ce886a6bd51cc229a9669e536842d05ac7dcddb5d74b09d0636989"
                            },
                            {
                                "filesize": 6673529,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "05177c800c1d884d43d2eb66aee29021c584956bbccd6f21dcec44936f45c42c4d635c2383eaec740a336436fbb418471b64710a797625bccb3706a3d017df15"
                            },
                            {
                                "filesize": 4805553,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "48fa750dd0375ffadc0ab739ace833d1ed4f0e83e68079b09c30be26023fc5995f9187e2a8db78f939a438d2e7eeb5eeb9bbd52e4ae205d92cdd09195b5ab7c5"
                            }
                        ]
                    },
                    "fr": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 45177788,
                                "from": "*",
                                "hashValue": "34964b3f358d6ae2d136b117f1364e5fd7972c471a27f8b2fcfa2645f662df17e4fc0fdb909bef644db69e424f98841e5e01cc65185e831e35151bd3fa7d0fb3"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 6354302,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "c7ce514280075b1c1b0f04524149fb384b2cf7bafb5826f3151973a9344df508666069ea99040b1dc4fe2b535b423df8a63fc89a707dc2414b6d5c5271261bf9"
                            },
                            {
                                "filesize": 6673577,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "d673dd278af91d6cae478f31c4b7ed6ba697601a108ad668e4b5a8b658c6f87b71856cc583e054cbee0f5e780d7010c8203dafb38d2abac3c434810bba72ef60"
                            },
                            {
                                "filesize": 4805605,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "1d6e0c882c40eece754058a0bad43a9fd37300fb4852b8bd4f2064f5520ba1a78bfb50c254719d2c80a2f27f6bfa21b91fee3acd8816a55d9f61134d83338a32"
                            }
                        ]
                    },
                    "fy-NL": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 46180566,
                                "from": "*",
                                "hashValue": "b71f2fcb05e2e0ecea545370760a35d556859b5efc889d8026bcae56c3cd92a03dd62bfcf60443e245d416039dbd2a121007fd2862bc47eeef5cf091e1870140"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 6354298,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "5228b7e00537762e7ba2966fdeae50b944f37f4a663a289db43c06bda7a3216e264ade04350d473c0819ffc7e581ac278e3433f8cfde99d6b2ae529bcca06808"
                            },
                            {
                                "filesize": 6673589,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "473d1de77f1c23982cc1aa022de6c0b868a23fc708281d045d60ebebc4b1bd861b3f3f92a7f4f9dc030a724f8e34759731481c5b7683f8bcae611b691e046bc0"
                            },
                            {
                                "filesize": 4805625,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "cddeca8a300142fa5a8bf9352185bab5534654a60f7be1b748c3117fc150978cb202ae8bc97f0ee062e40857315e5684bebd65887326a87cc8a3e62de0d070ca"
                            }
                        ]
                    },
                    "ga-IE": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 44897096,
                                "from": "*",
                                "hashValue": "0a0e41ae5c35d8e106b365d25ffaab07db557148703fceef238b019b47c47f129d19ed609883e559d07558c026cc89361e9df09b794a154f8911e962ebc11042"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 6354274,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "ea2e43407be76ddc40327107e0a11526ef2e911186e8d6e6d41e908a60daa68b3c70f751110bd3dae4d2af067c24768217ae812cf42a42abe121acb45348311e"
                            },
                            {
                                "filesize": 6673553,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "9e2f13bbc9cf1eee673da1d50dd8e5076f73d3c3ca0c8a85b72e42fe10c185f58a5f0c07f3e4451e6735c707992cf6dbed6f65eea8bde2f6612d21293671e052"
                            },
                            {
                                "filesize": 4805589,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "93e5166b862ed5aa9818b851bc441f22c379a53632041d9b795312442f006ae09af54f1e40331cec23441278d884a09b47a3081d715a2e859ba780213240cb67"
                            }
                        ]
                    },
                    "gd": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 44891428,
                                "from": "*",
                                "hashValue": "8b297325bf157f6e979384b144500bfc3bfddac200a40971674db5a7a6ec52fefb6c09c5fc5fe46be652fb6056c630e14c5e7b554d1e03efa81f007f28a0b40e"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 6354266,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "c50ec81e5ba0efc3588aeb3ead232160be4dfc489044aae83eb16436e5d0e6beeca7d5d843220b786ac8fbada028cdba0a6ad86a03d8c261877baa029d5fe124"
                            },
                            {
                                "filesize": 6673553,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "bbef3aaab7d366ab3c57a6bd4ee26405b884d71ffc654ca0d5909ad3820c079c24d99496f581307f318643f4311ec5a54626be9a17e38baf2220a6ac52020cd2"
                            },
                            {
                                "filesize": 4805581,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "6089031fa5409e497afd4f6e32e4f70145a0e7f1fd2a3ce17e269b52a236c174b0429817428ebca48c43385a10aad39c1cccd3cfbf93b6b57176f9c9b5738b9b"
                            }
                        ]
                    },
                    "gl": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 44883068,
                                "from": "*",
                                "hashValue": "c02218eed5dfdb1130dd384319ad422d0a6e80ca435896f35bd6aa6b106c80dcff3fe588ff638bc12b711bfeb0d155b585e89dd9e6bf9224b44367dffd13a83f"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 6354254,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "ce0b5ba984bad48309f59e7b060aafe3c6f67c38fd4771322c94b79029ac941bc3a661cf8b93e9d005edd979a53863dd9104a39915e8111236a4770f6a8c7881"
                            },
                            {
                                "filesize": 6673549,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "da7c4ff40f7285cc8221519870348a9fba7fe6ccacd7a1e881d623d1fcee3cdb3b05299180a154361ef28e51b7a282627569e7b851b5d7bb43edf2c417765201"
                            },
                            {
                                "filesize": 4805565,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "6ec58a65892c2c3e66b0b0e96e00b658675064a081f7f8957642cc40e67a3122b24186e5ee021b221c9776ef8f809735a6f8eecd0253eccd8c1ae1217efa3d4b"
                            }
                        ]
                    },
                    "gn": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 44895272,
                                "from": "*",
                                "hashValue": "25c2140fafe08a5155fd0778ae8d2cd24805c7cdcf565b29cb02e20966e7221002e162fc9f89c9b55666652a3afd49f010b31017ee23de13b2867f3af5c0793d"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 6354262,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "459315bb2a7cd8206867e06753361de59d41d2df9b310cb295ae714791ee4d192c1ebe105e2a5f78b136218eb8c1015e7473d4735cd4b4370b74ecf149f2ecef"
                            },
                            {
                                "filesize": 6673549,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "fc4b8ffe7e9251c3d899588d8fa039cd37c35ac54d567cfcd37aac4e58f3ece221746bba27084de9d21159a250a8dc4910e883eae4871dd90d3ccbf720744a20"
                            },
                            {
                                "filesize": 4805565,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "5b3c7e5f3449e7db737b0719f022f931605a9a7f40c51c92fc6e865f84e1941ce9be4a2c39938059abd0688b4a44e15ad3102a378e8b02393e7bf9e0c4a4deb1"
                            }
                        ]
                    },
                    "gu-IN": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 44902356,
                                "from": "*",
                                "hashValue": "fbf2ebfe647f7f2a69851129aff2f22a0b65bedfb03b3c844bcfd999aa6c61ea5c2e3cbaf950d9662d0e0041ebd7fe7c6c0b62c44f63559aa1afacb652ba1d9e"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 6354322,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "868019611ebeb6d90094722c8d6680237c711ff0a49dae82a51a69e73fc22ae9437a23f605901075042a9443eea498d617e0d76e1166f102d8f969b6b9700837"
                            },
                            {
                                "filesize": 6673593,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "6c716a174adb539739487be5477d963bbf71b7ba1dfe4c3bc3bdc6ce88f12d0b286610a09b21c7c9e5013c4cec24a3d28fb6790c6310d748dea177bab21c1065"
                            },
                            {
                                "filesize": 4805629,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "9054c5dc4ae7b02a65ebb29c54364f2b108434addd89659144ad4c394ebd7a5a1c9b3c2f1e8529a6b0242541d4fe4cfd495b9b997d6a3e26d1edf9359a8fd64f"
                            }
                        ]
                    },
                    "he": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 44887284,
                                "from": "*",
                                "hashValue": "628827c7eb1d761e311aaf4bff5ad7ecb239ad46a228858f63869315aa1770078ee4e87ea4761ddcbc6715ba938c495570458c1cd88e882ab3b2dc4786ab1429"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 6673545,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "1210ab6585bd6a7888d88cea298961aa9f36bf96e301cf10ce009de596289505906f845a54b4a5e8041cd6be31c2c631af48c73b23edee169dc63014f01f4d52"
                            },
                            {
                                "filesize": 4805585,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "eeacaf9530f6e6b4b2ad87d4087a8384c85a6c6eb7c81d20a9ac2ebb7348c77857b09a140659c2a158ab8ccfaa7184ee26fd25311a7da9efba623090efebfbd2"
                            },
                            {
                                "filesize": 6354270,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "f39876d0e2a6a0cd290a68185ecf4284369b79283ad5dc5e69ca985eace898be8ebad17b240bbfc62b513fb5aef4b87071df5683214b922fd4563ceeaeb8500a"
                            }
                        ]
                    },
                    "hi-IN": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 44908836,
                                "from": "*",
                                "hashValue": "186506ccb591e6f666f2f952800ea08144f9ed7bbe87db609a433e3d6a8d032dea8ce89e7f7770882423f51908826c4382c8c94943e30ed765f2e4036c6f2871"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 6673605,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "b1beb7dfd00aae59e2be9ea7f8b1428b10f5ef6e2d9d3dfcf66f42d31ef046b78f3b786d1b2416a557cbc2afbd9a4ce7eac755a0775af0dc633ecf09ed570d85"
                            },
                            {
                                "filesize": 4805641,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "75daa2e8f5fe4ec09b8679077afae554d43e60f37dd36cbb64762885d5037cb5801a73d9170f1be97f95e571fbe0cd3e5e29a36410136fafb9e6b5863dc11728"
                            },
                            {
                                "filesize": 6354330,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "30ac3ea23427d839c60081ba83d51b9ba8cef8ca4cade82a3fbf5d90b8a78ba0543cee25b6ec13d4bc2d7d8c54e48b89e62d31767a82ef3780080edf3817547c"
                            }
                        ]
                    },
                    "hr": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 44892088,
                                "from": "*",
                                "hashValue": "79347888a690781d7f85676e69818d0c13552b25ebe087ee8f93963ffe1097f14a5feca5b31ba7989875dd1b2511c2c3265a44c6182527d3c10d8652dcbc4435"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 6673553,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "900c5e46bd01421dd2d53fc1f73e6ebf7803e7b07e933c29447bf11f2004e08efbd02f87d5b15159c42eda5aee5d08c6be76b98f8185669b5a9030318836f1e0"
                            },
                            {
                                "filesize": 4805581,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "1ccc41c6348eacb2e97fed2f2db24e2e3a42508da05a9895f867647b6c9f493cb62ac35bcda47cb68bb4ba06bcb5cc1f005a8de8bf041189728ad252b6635df9"
                            },
                            {
                                "filesize": 6354262,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "8bec0590583c336a952319f7957e6bb5bd1620a854359a45d5f40b591c6697034778ff5b17b71d7dba9baae3ff500f58f99269197e7d2c609396e9e324b4813e"
                            }
                        ]
                    },
                    "hsb": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 44897516,
                                "from": "*",
                                "hashValue": "f1f3efc7a5b186134f0867655f5370434d07029d4b923a81fba685dbec771ad7707095eab1842b99a79804e782dc17897c1476f9d91de650a9f7fe4c447ee403"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 6673537,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "1e35210e74f594eb80894234ffb3309924b33930c6e4c070832ec4cf29ace11944f9505d576f1e5ae1c4b1bde52aca2ddc5c250076f9f5c21addeb9fdebf70de"
                            },
                            {
                                "filesize": 4805597,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "452a846514f1633a24c491e435b8807bf3d7d6937c06b9564e124bcc2848824848e5b2f24308c6583bc0b41a8785de8e011447b32b319d5c3b5104225d6fe476"
                            },
                            {
                                "filesize": 6354262,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "1322e4eb66e00ff63c25d9540e6e8b23490f39934c5063a7f79a978b1041492137e8f40e7005a5aa3d7436a1c434e7b1e936642b6f0be839be2039d8c18e7732"
                            }
                        ]
                    },
                    "hu": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 45447148,
                                "from": "*",
                                "hashValue": "2b5f2d49975e2b5c1e5e414d67f3c5fecf6bc9ed7d1a8e4ff4c9d03c76f4063f1a6c40bfaca1eeaea55e3ec29d09b398e46ce8ae08d43a7c00b137f3e3d592d9"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 6673549,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "27a2c439d6653eaa0ce12fd69a5996353fac88bf94e9c433d71764cc86e2623ad740aa9e8da0648fcab160543c3839ebf430d5b1937404f0aeb08522aa4a2d6d"
                            },
                            {
                                "filesize": 4805573,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "52a263e443dad9918c552af3df488655bade995ba6968173c705da5801d18956139aea1552202ae94d01cf80a83d224ba2546df21fedd0ca0757635e55a69118"
                            },
                            {
                                "filesize": 6354298,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "b75320601ca0115ebdb04566a664da2be66d4d8705e40482d6a2056dfd301cfc319b850313a48342bfd9b5f564df8edd80d91874afd38def2b2ddfc10b3c38bb"
                            }
                        ]
                    },
                    "hy-AM": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 44902496,
                                "from": "*",
                                "hashValue": "0513620f015d426d4990f8ff908ecb3cb654f51cab9b9cc6859565ce45bebdace93bd66d250f5d0d6643abb4b58a6bdd982ee285fbc0f1ba8f615876e375cdca"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 6673561,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "a52ebdad5e16cdd5fa960bdc880adc0ed604451b7e2e50caa03704be699130736aa783aa110281d6bdadd9fac0b17f22a0620d1315d599be9d6cbd85e3069224"
                            },
                            {
                                "filesize": 4805589,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "c77282710bef68bad6946bd760151011986ce81d5f48e0cc53339393f8cc2f6f557fdf6cd5bb422c53a019d70755cd4e63f12754fd0156cb118343d42a687829"
                            },
                            {
                                "filesize": 6354310,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "d44f2d4bbaa0ca26585e31c04b77cbaa867fd02b30d300d645fc39796f72cf787087410b728241ecf9ab3263f1a9721852a86513d2e7aaf3d6b0d148363bfab7"
                            }
                        ]
                    },
                    "id": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 44976520,
                                "from": "*",
                                "hashValue": "d48ae4e2712e7666d9e2e41cf729bfd510098a10c76e6d4cd09aeb4be30d4e44b16f1b1d93c5300fef261eac7fff1a68534ed8de0e811ae6bf71fc741629e6aa"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 6673541,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "ef8f7febcfe8ecd46aa33ecb4d9f06942e66048b20e40da6dba7007fa136b9b74a9d0ac1e03da2b156bc35a582facb62ccc483197ffc95b27bf888b4ab2a311d"
                            },
                            {
                                "filesize": 4805573,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "f222a0ba8eae6053a9799141f38c3849cbec43a20575ac6693a9926b3467f3afdf36ac3084d81117d6a7151b5381b0d1b7576b0cc0e3eb00d27b26e7529fe809"
                            },
                            {
                                "filesize": 6354274,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "fb262261c7984fe59cc83befe657e3deed692049050b250277586a7c4dbebec1852945f745993003b531aee00f8ea62f4eaf49d434297b0eb96ff78c965d5c09"
                            }
                        ]
                    },
                    "is": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 44885092,
                                "from": "*",
                                "hashValue": "c08653f50da86057630508b38e07eef213e524cab42cb87a0b641e8ecfefaa8cab050dfc7d0d9acff89d1bd101943cbbbbc9c91f885842f2317647a50e52d913"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 6673533,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "08eb9ec9005de25bb47a39c904ca771638723ab1140ed18b9b96a9852606f926f1672e6e67dd58a693dfcda3dc2a279a74ccd1b426d4f46ebe9d6745b7234cd9"
                            },
                            {
                                "filesize": 4805561,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "345150f26b2cab57224e325591d41b46276130fad5cf2873f6cabcf85bffeb43c9246dc91008acc9816d24b5dc11824438e41fcc4c52e970566da67a86525ee0"
                            },
                            {
                                "filesize": 6354262,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "a9d57c4e8671b99ab00a56494af8679ee00b7ac984ddd6fc83a8a11a71a8b6fc8268b9814ea20cae049b46c723ca304edb96b2bcfb93c55460f971ef5d1462c8"
                            }
                        ]
                    },
                    "it": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 44812924,
                                "from": "*",
                                "hashValue": "a0a8b533b20c33f58e87c5b70f8cfa62fed599661a8d5a815eed14d93a482c456b85ced7bde50c9bcc6437d6a7427ec0fc41d2749adfa75f4601c6ad00b72bc4"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 6673501,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "6eb7091bb015ceef169f098b175dc71b9a18cb3baa10f0acf9aa1b8f055f2bd183d889e927fa57b2495ef43209da93ad6ad239968c6782371bc62c970ffd43c1"
                            },
                            {
                                "filesize": 4805525,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "5b7b46b35ce9eb81b743c0bb7a1b6dd4ce5a9a95aefa9582bb15991566fce182ef288c67c7279d3e3b2daa509b21d2b40916228cf7b22a313c2dd5451527badd"
                            },
                            {
                                "filesize": 6354214,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "e42c1b2b9ef583e5ac5b5f8ba789ecbfb73cc2e6c8c39f29cfe1c78adb5de276bb995e49e93a67f08904388ab19213d2c5aa6b5503d20d021fca2cc4c2d23dd4"
                            }
                        ]
                    },
                    "ja": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 45078718,
                                "from": "*",
                                "hashValue": "f0e77c55683e1788ba28aa911f2153681f53ed91026cb4cd71782478b53e00c8eb272377e95d544bad54538909681db8858f995d188c0cacc70ecc4826cb6862"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 4805609,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "d0e8bb07396a24081ab605d9a7908a0b2a4acc57518e720cd1e768bce82e254df283b1239d895c464adea2eb7dfa4f9b267b58295bba3406cca3dcdeab58782b"
                            },
                            {
                                "filesize": 6354314,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "8b3f171217b85494e4d638a20939a49528bbe4da25cfa20f0183781a88cfd6f1e45690825f38e9c65c6c562de8937eadd5400db3c74d547bf3fcd7ccbcd6bf99"
                            },
                            {
                                "filesize": 6673581,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "42887c2703329d3523efcf05c767df64b2da29b106f778be007445693fddd714533439439857262b4828185ac7ef3436933f2ec014832ebb4f8533d8e2cdf271"
                            }
                        ]
                    },
                    "ka": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 45079024,
                                "from": "*",
                                "hashValue": "ae126ee95537b7433c4933d8c7ed98002d2f9ac08e78ec71eb288152dcfa3e83596b9c619910408db9bbc7e34442c7e5860d29a808e815e5e4fe7fffc7027e85"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 4805637,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "ce740f609fe7210d7e5c09e440991fd2f240f2f1cdd839bd5df287de199ce0d5242592093a34d798f8a5345a26e21927d4b924c8c0fc2c904bc28063e13b6673"
                            },
                            {
                                "filesize": 6354330,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "711d21d609b85dcf4eab1bd8674ccb290f0e1de0158fc33062bd738ffcfd813620b83ae50e2fed9929abd7a551f25258633c2a185cb32c9e9f4a586c83776216"
                            },
                            {
                                "filesize": 6673613,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "1da8ec61b7280ae479e3207f1da8b3c6a1bb082b7ae37f197dec9610c5e610b3440361918c84450712816eae2cb6ddfbcdd39042812b139cb26d7281aef9bdbe"
                            }
                        ]
                    },
                    "kab": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 44891440,
                                "from": "*",
                                "hashValue": "6111fd2128f96e40f119b264d1f8590003e90b9b46a9fce9b6a5f42a5d85aa938f6028ae39c6e9fa6ae657f12d1d56e5a751a2c59f2fc4000f2c8935f2bb2a08"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 4805585,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "b077fc83e7268d182574f1401003f46557cb447cccad6a3aefb6005fb1ecfc6bbef9bcb8eb6ccc6d21207b7e45dd6101003885a96c5fdc89d86c04bfbfc0a2d6"
                            },
                            {
                                "filesize": 6354270,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "8660ae577d1c30cc7d41d1f74a666bf886b87c12aadbe2604249a1d51098ce4b24180939d7d35f10f74d43c074ab676c84cd25df11746981d90a33d6b9e42779"
                            },
                            {
                                "filesize": 6673549,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "0ca5f252799436ca586f0f8703cbf2af15df0ad1b6c14e5913ccfedc0402a2d2e761476d11521159bf0e00d07a3c75b55885daa08b0b369ccc47fe70b43fc0fa"
                            }
                        ]
                    },
                    "kk": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 44901756,
                                "from": "*",
                                "hashValue": "9018d893f005edbd049af2888142321fe30495022b2c30ee32eeb2fd3d7ffcb8f6c3a8ada89138cfaf67b9d815a201b46e73e82d5ea725eb2a328f7d2790778b"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 4805629,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "830909291d36f57e29235fc805df00912bd1d8e598efb147d079545ebf40118a6f23c1395bbc1e98cb205970647aeae0b473444f8bd79ea3a0660531d041c0a1"
                            },
                            {
                                "filesize": 6354294,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "d2af15586164a2da7a73560786609513abf2f8adb85d370a94b99037da77e208780550b20535de43729065d9b2c4bbfdb763096d56d818204157f45e230368a3"
                            },
                            {
                                "filesize": 6673589,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "b491ce8d627ace5d4ac5a315151b936e381c9a8eaf0a65e3c6bb806b30ee87f8c21225f74f234f812fa63a7abc6b78a4016e862eebbd3d711f17a50d915883cb"
                            }
                        ]
                    },
                    "km": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 45088634,
                                "from": "*",
                                "hashValue": "92c42c7473009f11dc69b15556b23e645c64b5c48dec35edf20504d45f3acd3c2fb1377e192a76a44ff434a904feb0b71b1df957e028b0e5f8f24ed654a59967"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 4805689,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "97c40dca5cc124f56db8841a3afd1a39c2e38741a660b34760e7b14f0c5a7a51069dfadd208c7c6c176a9beabcd399f9290737b66936bcc52268c9494e242259"
                            },
                            {
                                "filesize": 6354362,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "d755eb8b237199fe810df2488cf76ecfefc2c5b6a28d01aad19c9a9daec1b764d09cc053833c5b1d7abd88823155c14d582acedba91fc7cd6fb30a2473ec5047"
                            },
                            {
                                "filesize": 6673665,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "90bad71a8f8825ebc7cd8892c20995cdf30147db1d211f370882a9904ab2f261accfa71ba532e74abcd3bb4a66d28ce1bb49c627dd2ddb798a3af6404892418f"
                            }
                        ]
                    },
                    "kn": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 44911520,
                                "from": "*",
                                "hashValue": "1c65f39e8a11332ccbbb963a66513f65d2972293c4e6ce2d51204d059cff01cef9ac54637777f6616360510a73fa0c9d6ac72471010a144f737a277c418f0c50"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 4805665,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "cb36586cb3c3072eab1ec2b13dc1411b64d713e9ea593c667ece8fcf8b1f1b4e440b8fcbda5983388fabf37e7082252cbe5930d111a3c6ae915a6090a041d35e"
                            },
                            {
                                "filesize": 6354346,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "52f891d0c0458385473c58c240119890bb146610455333579aacf24c29d8a74d8f2c5fdaad29fe935cada4af5325a0e99c7370cf281189a775b65a9a05a15e35"
                            },
                            {
                                "filesize": 6673637,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "dd7e5cce5ae1c6639ccf3bfc6ebf64725af345338d5620e5380d838d7815200f321727795734f83c56d9727ecec8c879521e7d78eb4310f65027ca2bc4a18eb1"
                            }
                        ]
                    },
                    "ko": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 44889368,
                                "from": "*",
                                "hashValue": "9ddf94dd8698e23d731e22c6273a7451bd3ddce3dd1fa661f88f91d4691fdd4f04e53f96b90379f2d7e4a914730cb3d7d3bee17e5456f842acdc5123590aad7b"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 4805557,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "ed9def61d501bf75981db3daa16979b81e0cdf41005cf7113309dbfd2bcd968fe5ad198f90ce3ab8b7861356678a38f7870838a2c8a09ae1c335307941729e94"
                            },
                            {
                                "filesize": 6354290,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "8d1a788253c1c59e63f9e86dd6f6f13456d50f7e69ecdb6dc85d8dcbf62d2eb715aa8eed039ec26fd5c760fb698d79c47815b4c50934b87d99b10544d0cc2397"
                            },
                            {
                                "filesize": 6673549,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "a856b14f781af6868d6e63ea9baa1f6fdf82b7bc1cff031b0c9e04a772f9364200537c1e4a1884b42c097dbce548fc80969edbbc44c24c5e03dbacb6edea0197"
                            }
                        ]
                    },
                    "lij": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 45067458,
                                "from": "*",
                                "hashValue": "7e77fda999ba473373194b72ecb9ece523e78e1ebbdb58fe84362d11292aca3037edda069997cddac6c5aa493344d40da4c7fe0e9dba6fedbfbb67d64ab330bd"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 4805609,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "22c0d14745f53e2c422a7e4a1e5a6ae7c317aa3c5d3e059d2a55366eb945232771e0f53d922a5f24fcc63a346d4f92c040ea9e7fbcf518acf1d528d3028d7783"
                            },
                            {
                                "filesize": 6354282,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "d12970789d48156b04e53faad250b3cd97129a6f84dce83dd25095c0c9f39f6ebdeeab6bf0d4249a8c9472bea3c5bf1564b94c9775b8821b54857a403cea321b"
                            },
                            {
                                "filesize": 6673565,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "8c78a4d8cdfffb2b84089c1ad5263d2b9836f5e2254a39625079ccf4313bf2778095a40eb44b83dcd6d8eb8265153e85edbaf2c66178a32a680d74d211c198a7"
                            }
                        ]
                    },
                    "lt": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 45170184,
                                "from": "*",
                                "hashValue": "07d97c76e17e185978d28285dc2c4241e44d53c3cb29ca92d4c2aea65f5266c63966dc38d9fa5af3f55e7130fae8a5f410c6bb41630d30fb8a2db64332049950"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 4805601,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "d6e0de7d1355a2be95b917d9a14c4d890f9da57076a0be2c4ff0efa54d686c46abef90b51dd019b349cf4622da9faddc23287d9c7bc008f99c2fc91421d4cadc"
                            },
                            {
                                "filesize": 6354290,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "ec2ff71ddc8ddd3217406d20d6e6cab289b12f96816a5f08903e3bce8c1ee2a07e2dbf9388778da0570f26d750104c488466f12941aa15c9cb2f73233465b3d5"
                            },
                            {
                                "filesize": 6673569,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "6b380a05efd02f5434bee418748286fec1bd471b8923a5d54c672f3766dcfa19692c01064a3ac3bac2ca976188c1a4b5dfb8de62af27f41a2ba66676a2c30b5a"
                            }
                        ]
                    },
                    "lv": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 45169930,
                                "from": "*",
                                "hashValue": "91797628dc8ea71b058fd2296717ee19d558cf58dd7455ec554cf2431116e6da4f79c4495e7a44c65ff7f161475ca2140d549c90b96009765bf0b455c622f525"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 4805601,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "bc3fe0cd2ff4ea3b3fbc604b14b9ccd4eb8efd76d04ca76a5e083442edde519e1ae94741749790fc964776fe1ad710dbdc06c55827cc55907a2484e2737b6686"
                            },
                            {
                                "filesize": 6354270,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "dd8eba8474a93f740c45f4ca26154d4e1d09041a971dfef161b5ae022ba340bcfdedcf3934e57f5190f37b1615cd3c34c1c4106acc3934da7de99c29ddc54f16"
                            },
                            {
                                "filesize": 6673569,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "a1150bad02f2bb50aa9c5e315c0bae1413f475d454599dfe444de5408c412b752fd09f82e4af272da773b9db6c2c31c1b0f5565c7a9a92d484aefff23579d559"
                            }
                        ]
                    },
                    "mai": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 44905320,
                                "from": "*",
                                "hashValue": "6dd2e309890b0d08963998cd4ee490b8504f56c17b5478140cd85ca954114165e40c3c22df2fc143f8eb3f48e01c8b66b7cac1f11e987d14496d460d45d1ed99"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 4805585,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "76e573821e9eb7352e4eaae16ca09b7760b6c6f2962484f5becb1cf07876adb87dac448987764cd2733650cd25b4e1f53bb65fe62a5e8a3672e23cc2e4abe360"
                            },
                            {
                                "filesize": 6354286,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "08744128c84ba1f807e668da08a621fa0b2d4412a4d46c4511b16b848885476d18a029612340bbd43bb286d509d363df5c1715a78e2902adcfc406a9b5321aab"
                            },
                            {
                                "filesize": 6673545,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "db36f8341b636a1f19123aa80f12da7801556d6fa3a0c7057ffe69f8d88bbcc0ded5aba214aa782953ea8fc0a72f629f979813aef6aa475e922e12b328b272ba"
                            }
                        ]
                    },
                    "mk": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 45328004,
                                "from": "*",
                                "hashValue": "8dfd1a1f5a3ddc12c864bc555c794f762f1b86fba5691e165c32e8e0603f2834a86cd3a048b7f7e7bcaa63ea70abe94fd816d4686ed5a0d21ceac344f1e95dbb"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 4805593,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "7ddc9dc676cc8424672502fc6704f73e0ddc574f6378f379149cf99cd6ef654f923ff0c8e4af44c5962659e1433c63e87179e29913c49e8120805ffe46e295f7"
                            },
                            {
                                "filesize": 6354282,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "0c6827ce880e35bb6d9ce95d43f099679b14c1f6a27f1b612be4938cf8b68e9dcf34d153b81dc443c91f16466a3ae6f68d2293389e78b3e98afd9ae3ecc57d9e"
                            },
                            {
                                "filesize": 6673561,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "bbef4053e5e9702dbbe1b512c0734979c6c2ed5eb094a9e958c5e9ffb13fbbeccd7fe993680ab7e4063711773d2941e581dad6b2585c88b5e1403bee99edf028"
                            }
                        ]
                    },
                    "ml": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 44911364,
                                "from": "*",
                                "hashValue": "d48a31f96059b645860f7f328afe54f2bd9f1006280179c39b120c91bde9cafc50ba9bd46e0918695f02b78b877799f6fe0a7aebd9d8ad4727fc9c19ad63a766"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 4805617,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "ab20e80d49307a9c37fe232aeaa1191ba08c193108dde7aa31bc7473de0760a1ee624224b94a50f7800d19e2108aee504901c5b1a69143bdd2953d5e76204d7b"
                            },
                            {
                                "filesize": 6354326,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "eb0117755f5ac9f1700b29ab6238c4307843ca031b19e86dbfe023955117d125de518d51fe41db65af595bb933772597be568464e74b97b1d32e8a669eb09cd1"
                            },
                            {
                                "filesize": 6673597,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "75764308d22797e6808da64156594ce8855068e97bff3a50c9784fc1f6f2416b95b8a43e4ae398148f1f928e2c86ca6309ad4d5bdaa5efc6ca54ab34186aa4eb"
                            }
                        ]
                    },
                    "mr": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 44906380,
                                "from": "*",
                                "hashValue": "64b4c1a795af255e5adbdba1580e7f4586927a9087ac6606a0a9d174c9b51e057edf8146163dd8b5139e45f8bc1d9838d9951c1a28bc5c46c545a7e6cded1897"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 4805621,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "91ba532e6e114c12a92b76c4f7308c609e93e23c11ec007dd68180c5b2083dd823ef20948a6e1ee9c41c7f5c01ba6e6146f4e0b6399dda9e51e5ed7a9793948a"
                            },
                            {
                                "filesize": 6354326,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "b33c4ec357e9502475fd9677c41bce62ff7f4abafba62aded545ccb541f5b87ba0e51f12aa24bc067bfca3c7f9a70b0ec2470d897618d43b53aba22a6026e8eb"
                            },
                            {
                                "filesize": 6673585,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "6d46a8a467ab3a490bce6cda7c4e45a1e15504544348914fa7b4be9a192b0167c4d478f32e425b33863592557047214e95736a343f1afc4a011cc4c8a0edb1af"
                            }
                        ]
                    },
                    "ms": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 44887856,
                                "from": "*",
                                "hashValue": "781631cfcb128a7640fc1dc1ee72a2ba869aecdd8bb41e98ec24826055cd20e73fffa1f43c34ab2133a59812e127307305fe8358d89acc6041f282fea38937f2"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 4805561,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "ef55dd185dbd357c573e8004a1f49ea3a65a519c3a9708e0c0768116a318b3e066259e4e084c881dad1352d68f67309edb35228dfabcf01bc7a55174f478edcf"
                            },
                            {
                                "filesize": 6354266,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "9aa3200bde24296035c4a46791ecad117c15c7c70d3842d723982a854dfbea4b16885e32a23dda575a3cff522cd293714e3d8c4ac069cf2764f6158ca744d815"
                            },
                            {
                                "filesize": 6673541,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "c1fc52b70f1fee22cd407e3ba50952a200dff0be8a1cb3a2e2ec076bb64abbe509ec73fe0dcb8fd7dfba0cf86cb1155450a639f7802faa78dd12a0ce912f30a0"
                            }
                        ]
                    },
                    "my": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 44909888,
                                "from": "*",
                                "hashValue": "7302ea414e8f050fe7b22acc965073c592b1d6cb478a8db5dbfd292f3181425e0045a7e08f649613e6cb4c51214f2c5543f0736b1d7e3cc3a5106f5356a017bf"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 4805637,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "3dd4fad0a531acbf75983633593af8e3c6faf2a647cc6604adbba12a796059e97d02e750b9d6e6405e103035c5a7db64962e6c70ceb3b4cd9028222b2885de51"
                            },
                            {
                                "filesize": 6354310,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "58c3fdf7247c38d4d2d0086cee05b2ac8ad2281442bef6e0490c5b64253a340b04800b6dc05ccdb96f1057a4017e92577bb89fc4316684921e8997e1fadc7d6e"
                            },
                            {
                                "filesize": 6673609,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "63dde608253ad28549c428f45844065e8d9f4d9bfef2d8258b744aaf3ef1a0b16cf15d60ee88614b09e66eccb641569866e2e412d80c88491cb1c5b14ff3c38f"
                            }
                        ]
                    },
                    "nb-NO": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 44884288,
                                "from": "*",
                                "hashValue": "e8af4ed347e0ef8f16dc05ea6c43a176655af7c4149abe1f993f00ac236e76d92065603a4b0ece0e27145636d219a136ac95d6ca134292f8f733cf67cb80522c"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 4805577,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "90775190df29d0aec78e42f4501b5136185863ad6bf06f711a16de84bc9a1c5f38dc1eb9ced9661422e3d6908c1f5435c3ed0c9cfa61c6cc05a00fd25a639fbe"
                            },
                            {
                                "filesize": 6354266,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "319a2b9e9449e6ab51a16be9d7e8a8aef78817ee2e106201f64c00e632ab18443bc7e01ce3a363755dd27efdec9558988e9637d572444bcbc10cc23c93c3adba"
                            },
                            {
                                "filesize": 6673585,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "981bb06b8b95eafea6920b9f5dcee9977521cd039399e5a819f28de9b4529a19dce26c1fa131d0993a704f70f2c3b701e1f6f7a60ec0282d7bfdb4880a226613"
                            }
                        ]
                    },
                    "nl": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 45561148,
                                "from": "*",
                                "hashValue": "232062490384072149dbc10efb4ea48fde3658bcd25b1e590d29a80688b235bdd701c3b5fd1d1ce9c90ca5d63366460f09f55927cef40b226a4a107d557437c8"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 4805589,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "919a273916a7eca7400c9285239b35fdf52491121d410807e70cccf5381376a70c22795c15ff298783702e3e4aeba6ca938a12840ba9c6d8869cd5f266180d2f"
                            },
                            {
                                "filesize": 6354286,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "a8e6116e76b14866d300695605a9605b688f1e98a6c42eb6d87f0c35734998d8f514226395adea72da8235976ae0bade9dddc337a38c6be4b54df5deff81af23"
                            },
                            {
                                "filesize": 6673577,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "f6cf261801f6eeedb0226eee55c33c7e103b4e775020274441284cfda519996c3d145d81755a1710b4217ca0cc025ca4929bc7fd27ea05cb9ec1c51ee1aaffbb"
                            }
                        ]
                    },
                    "nn-NO": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 44885636,
                                "from": "*",
                                "hashValue": "dc46a2dd0a274421816db49209cb27c1d8f8b6c23cc04c6f5be68e7970d45e7bd7c067c9500d36c19329a86da62061812ed136c5badd66f870cd7fa4433b8178"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 4805585,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "20c5c1bb50bbfdc1b196965bfedcf3b63603e5b4300ffaf23748a2db3b6b400eb0eefa2bef3fa2571ce62b835bbe816aac57adab0c35d71166c4da4a85a3d72e"
                            },
                            {
                                "filesize": 6354274,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "4c7653e2e5c135576330c4319f1e01e2615ba449c424bbed674ad68e47a8f85ac7e6e41b44cb322c71e6b33ba3dc0c05590a7156e921c00b5e64d1b820610447"
                            },
                            {
                                "filesize": 6673553,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "52606d9bc8eb8bf01fa1eb46ea19e4ba4bcc1aa326091ddf61d67a7e843397a9a13d3bc1be1ee1dc0dc20b51f079089c2ca8955f26ff6bf8a0472d62263e2771"
                            }
                        ]
                    },
                    "or": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 45073714,
                                "from": "*",
                                "hashValue": "4d9aabf2b6be956224a98704f3904c85b7d59b596cef808fbd7d94e5db49d400ec5d43f5beeaafa9db23fea57af1617620fa4df8c4689502fb5808ef7af3f1b1"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 4805637,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "d63f4c407fa2ead2a6161eec6c1e0bc449cb9c96ab60f0b18e439e73d64ea3a8717c1a6560cbdeb68f1126ce1eb1fab29feab1892bcc035b910517c1f3a8d15d"
                            },
                            {
                                "filesize": 6354322,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "5e0d9aef27504d189df6db09db37b338def622e80ddc468a3dd31625983712501eb2ca2dd22b22a7bd740976f7970f5ef4de0c9300a38f70a9a404f3469c4695"
                            },
                            {
                                "filesize": 6673605,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "c2ccb5845bc94db223b0121c17f2e26e9e378b45446e6347e2dd39948c3dee17a391526a51f3d2d72b8a444a2e7bdb499bb5a1d801ac5e77d4dde30e64d7f604"
                            }
                        ]
                    },
                    "pa-IN": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 44895416,
                                "from": "*",
                                "hashValue": "74b6b5c43e815f3d09f13f7974be0676d1b6a5c6f16baafd4282cbe49a55d3dce57330ea9883456916b5e298e2020e5c0f21aa2d4b030212abd74be59445b3e5"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 4805617,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "6ac8a3a2677c1a77371b28bd848a211c454f16387cb5f837c4500cab390dfd474a17913e566b431a4b09701faa3ef04ab430edee0a09ef6e577b0bf7d0b5eb24"
                            },
                            {
                                "filesize": 6354310,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "a51e26fce92fe5c33462ee4de563c98105558de5bce6fc087d4359b2afe67b2f0b237417dbaf059949700c61f5b2fff68b108d951eda38ddd0e7cbc7dd3364af"
                            },
                            {
                                "filesize": 6673593,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "bbe9ce1bfd9cd8e1885c85e4af65090f3871c0a9deb41bf256ab13133fdb47a7f74a604ad11d8cd713012603773273afc523ff945e026bacdb56a4bb9bf7da39"
                            }
                        ]
                    },
                    "pl": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 45807772,
                                "from": "*",
                                "hashValue": "ca695d735d9976d1193f8a9e7e6ab697411c6093cef8e0d8d93407628839eb143f2dfca8a1a4efbda6ff79dd0edccb5608bed57276f1c95f131f8fb7237ecf9a"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 4805529,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "f8e21e1dea99124b78813ba8de6176a0b2f19204acdfb28567e4a375789fde86a9fa047674576910fb627567d131cb1c2ed1198a59e0eae5019c4ab3942354d7"
                            },
                            {
                                "filesize": 6354230,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "6e8bde1fafa6a0ad744870c689e7e4cc083c3d5035116bb8b85d38f540bfd2aa2e542c93f6d90087d0e8ae4d473c238318d0e747b6bb1aac2259817ec52dbd09"
                            },
                            {
                                "filesize": 6673493,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "17538e2734fe50e475954df2d7a8805ab8b9030bc9c108e96f63a403db82492de7a920901bf35e11a9af6391056c3df8f05b7215604db1ebc98b6dbf2968ec1c"
                            }
                        ]
                    },
                    "pt-BR": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 45039558,
                                "from": "*",
                                "hashValue": "f6fefa554cc89726fc243126d1b3adb3f4cdf062bf215b65a4e04751bed9d713c4d9cca35ab73e3c5c668da10061d36d9340cff05e5bd568560bfb8b4bcc47e0"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 4805637,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "9e7ee15ff6ca022f83c9f72271865f4843f8082c363b40751e1e934ff4086e8392b0a1261db1e4ad8c553522ff1f771cbdd989ffd5b87dd81ddecd3315ee0afd"
                            },
                            {
                                "filesize": 6354294,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "d2c522277c75c78d10ef1b5e118e89b36d0b0d5b41520a03d32f2060d35dea95c8b39e76b38be39f090282cf0d2bf14d09d1bcd011ba3ab092b31277475c5d7f"
                            },
                            {
                                "filesize": 6673601,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "bedcd64305e125e89dc2d22a8454cd522a15a585fa70350a90f147d830786f019b968537a7130e25d85d7ce8d78d7a6dd11cec48c0af85fc5f2a145322711ad7"
                            }
                        ]
                    },
                    "pt-PT": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 45065910,
                                "from": "*",
                                "hashValue": "e05e1d2f1560744576d689335d3b475baef1d8a12a3bd735ad126cc4b0a746a4a531ead5f738d11650cfbe157818b4d826ba77b2245f27d9a0a5b536c439f14a"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 4805597,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "5d8f40d6f48716a66ec7ffdea361a598e9e8e842425b686127fff45f2c593d942db0d2321aea24c4fb5e9ff4860fd7df49533e4ad23669925af2e34298847fee"
                            },
                            {
                                "filesize": 6354294,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "f44d06a16244d38d9f9bb56b4b6fd321f71400337fd17223e92c8ba11737ae7fb4222caa7eb76fb2235196e40044200249c4e1505c46c603322c163feac8bfbc"
                            },
                            {
                                "filesize": 6673573,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "73afdc8608d26747eb6c8de6c4a3eb8c4aee17e55ae6d4e307575bd69a890a3948a0724c709f66db4fd091403f7b4a510b3a82bee985c529ddaad2a892c1cfa6"
                            }
                        ]
                    },
                    "rm": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 45071288,
                                "from": "*",
                                "hashValue": "3fd69d780d5f835a85aed2dae8b513404e63f011b0ebe8851b5dc50dbf98c0dc14dfdcf438b8c166b4deaf8d17a4e139a8df620c77895f0f2a622b7fea0dd500"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 4805617,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "fc778f84cbaf87b904c0e286cda45fcf2611777cd494c163c71b9dd22c0196af8b8213580dc36fadd1ea693a400499a5d02f64299d19e3b7263acdf02e0971bf"
                            },
                            {
                                "filesize": 6354294,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "f786e34f82f479b76c097cc3616d22abcc3a829c5bb8a29e2d5a64e25034432f574629df561ebbecc19c09b6aa381cf4d262e7c26cb3863338ab78bdc2ffd25c"
                            },
                            {
                                "filesize": 6673593,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "cfb0495bd1ba27251fa02642e6d3fcb8bd538a5b46701fec02e6bcde86538d690e2eda37d025eb4fddbddcc51972f53e7ca5383becaa18164d48ebc761298ef0"
                            }
                        ]
                    },
                    "ro": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 45375532,
                                "from": "*",
                                "hashValue": "ea9a360b993379a4407853055c067478be63e28fa8d1a5a32a3e22aa8f31b3e88b753a2e26dd235556654647e6ee0bd3710b403fcba818efa927a439c5a0ac14"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 4805581,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "d0e88a7488037b329b82c26b68073df0bac6b717d38f33c19ef5b806a7a98db486a983a6dbc9dba20f79e1328add5f5a06f52753e95939434b08c07bb1bb8d6c"
                            },
                            {
                                "filesize": 6354286,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "ebbd6d02f92710f88441a0fe454a93f3b96072e877b67ae2a764f9b11a0ba37916f6859d338745f6e38c64410fedb78dce39ddb84655d6e8e55c2b6c4de884de"
                            },
                            {
                                "filesize": 6673553,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "9d5b1dd6d5b407275466c25897e7c76ca5c12b9cda37f631c8c642af01b2edef562158e92e7db7f9ca62c815c06220080c337e2c11cbbd16b96adab293f1415b"
                            }
                        ]
                    },
                    "ru": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 45330520,
                                "from": "*",
                                "hashValue": "104a98800f04a5f675266cac974ceac6eea4f2152eaaf72a4d63f19081b77515ce1cd44fa086c6f64e58a60c1b9bd8266400f8aff30650b91219331c2a30dcce"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 4806721,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "cac819c0fbed241e255b18301773709149f6c810f39b2ae4d0360964797bc3329a8c662b81433998d58fb3df3711a8da631a0cf002094516e4f6b1566019d609"
                            },
                            {
                                "filesize": 6359266,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "9232a5a8cd53e4b74b1ae5000637699e980e529d695250d61934b0f382e3bcd2f20ac7037769e575d84cba5d78439fac5fb69d0c9cefcaded40578604acad61e"
                            },
                            {
                                "filesize": 6674693,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "db4e03b0916292aeaf2989ce6837f5d2df6c22d5fb84fbb5008d6d020c89f8c9fe1c51e7555ec0612db5705ad6680b52bf38d6feac232be9b6932da817c53505"
                            }
                        ]
                    },
                    "si": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 44897656,
                                "from": "*",
                                "hashValue": "7795ed98a66f5e82e288b7fbb21d8db9e081f75a667322200c374519277146f7991e89544ad323f23b30d3d86582d0ffd84d158e3bb7d86b21e46d9b0bebc326"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 6673585,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "eeb0531458f39aff4580cf91fdd9bf4ebce6a78805764d713a608bf5275cc15c404f82eb0e738581feb0eda24e92a4cf9bc380b3ec2464f550dbf79f86dc7488"
                            },
                            {
                                "filesize": 4805613,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "68cd3650c8b1b23423fe7e8ca56f2b2f74d457660b81d2308e3b87a0ee982d3edc793e0f030a8bb3743f29689ca2c8d566924c7a47997331cfe68b9ce853217b"
                            },
                            {
                                "filesize": 6354310,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "901c1b465d90e3b04c5a7a58faa957a6f6219fbee370167e8bfd5ab60e7ce38de7d400fc9cf98d7432ac083f17b760579949cefbb98c227381500bf73df4ef3a"
                            }
                        ]
                    },
                    "sk": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 45583124,
                                "from": "*",
                                "hashValue": "d49c6e580782dbef328e3e4484d7bdbe679eec120218097a6f1472c99f9b3d27fa5875899f9b7e7fe0a322a2533315b1b323425627eedcd8f45d9cd8026f797a"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 6673565,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "3bcea32ea0f332570cc91c0d28d6c24832c62915f9fe38773d41eaa9279993d2443ec972a8dd1aab1adff4e71e4b2265b8a840cc03d15c5fe01ba2250e7f20dd"
                            },
                            {
                                "filesize": 4805593,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "be4f5163262d765c91541033fb30f3ccc784ee6a44e0421026260053d756f90ae042bddc0cc926d8855dacf67f7f0f52531039d6b9b1ecef7df7661395f1b3cc"
                            },
                            {
                                "filesize": 6354286,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "729ad576b11843aee3aab7eb9995fdac74936634b255f1beedf13576153ea74de2e4bce482ef87d319840f1a8544274ecb16ea0160e6f424ee896107b1cb668b"
                            }
                        ]
                    },
                    "sl": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 44893496,
                                "from": "*",
                                "hashValue": "58e4bee0dca44f77f434cd227adc9c3e0babd54d8b3091ba84e76fffc228c04f98d09740304ff5a54e2196f97d077192d700a74844973fe2f71287e5f16539db"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 6673541,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "4105a371ac5c229e8a531e23f2f4c40456fc68e99115327cff93edb1cdf7eaee5b4521b147bb26e56abd8d1784c9b3fe871bee5e1c5d8d14214b73c2dd53a7ab"
                            },
                            {
                                "filesize": 4805565,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "a77655a8a85d0416d8040774c2268077d7965e5c3792b1e37683bb788ee1e0cf0ff468b41118d01015ffb9628a2f0541fffe7d2ab8048581c55451812154a4db"
                            },
                            {
                                "filesize": 6354258,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "52d9c0d63c0b64cac2b1c8efa8532d1a94cade32ef229f235ffd3291be5daab86f064d4a93294f05bbbe733ebba552190d8a3323963d39e0e342b078c921a509"
                            }
                        ]
                    },
                    "son": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 44883596,
                                "from": "*",
                                "hashValue": "978d5e9c8cc3e069b674599acafa8780a5f024cc4b31f5c95e1bde707de8a82063ea25c086da2f33e845628ff577f6dc21f294f0c931e03abf6fe10f82e4a109"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 6673537,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "3ce2ddbbfce737dd93c4b264a97eb69ed408e3fe8fe6e57e99ff996fe93c6287e8028bc63e53506b7163b2e4ac3dda2721c1b585db5d64931030fa46a8388b6b"
                            },
                            {
                                "filesize": 4805573,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "e192c98e6c7c5f8d0444c6ae9704ab1b4f5a731eba276a0df6eb38e3a374b1d2f25f1cf4fa1c9470f437d6884442906f9f3d6ee65089031e0fe7b69f4ef2e47c"
                            },
                            {
                                "filesize": 6354278,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "434c4774bb8191cde2a27c9acaab3e29b98a8ff97fa567b3426b7c18dcbc89a1b38218f960039ae462f6fc7254a5ea839044818b6de53228e3c29161386f74c8"
                            }
                        ]
                    },
                    "sq": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 44897084,
                                "from": "*",
                                "hashValue": "bfda8d7376d8db188caf9c20399f43630191477ab9d84a1bda136286c52a171e4a302f2c11b75d7d6c87994150484d685b0e412e3115e0db5fb87369e115a1b6"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 6673541,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "bbeceaef8acf0e49dfce4134930e82c7eff6ee26cc611027db76b91eed8c2b0cabb567068e4960066f89f88cb33633320c7ef33f7b0de33864ab41087c8890f1"
                            },
                            {
                                "filesize": 4805585,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "872f80b850567dde4b67581955c3b48a4eaea04323693e5143ebcdb9c208851c1aceb5ae38ecd86540a6ca5772b66f680d6bc09a0e3ba56d687a84261e759a0b"
                            },
                            {
                                "filesize": 6354262,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "957c1f919224923253b7f9d3bb170b75a156a57ba5d9f5222e493af39c46417832de7be8ac68c71e18f7d73bd5721279262363218825199ec1eca40c0a606548"
                            }
                        ]
                    },
                    "sr": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 46021044,
                                "from": "*",
                                "hashValue": "ed1d213fcf6f03769f75c9b75fac6f47eed1d85e9cdaae008c1609a8135b85a96baa4ae15e50d7825288498cbdd33e2e4d6b44ed6ccc292c63787b68ee553139"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 6673577,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "f62f45bb1faf12f2a6357abe3834af7517f2770756d64a602d6ed71f4efc879c335012a059428e0ce100a62f377545727d58f7624455ce8ea2c38f5720531264"
                            },
                            {
                                "filesize": 4805605,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "9eb6449e4ef5e95232788bcce2a0af69266534e9e9eb38164e1479b22a3dfaea15e958b35cdd01482a8a540bb098537b3fc11c4a7c427bbd3cc1f1e81eb87a0b"
                            },
                            {
                                "filesize": 6354306,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "7bbad0b8a92490bffc917535fcd0fb6a77511cecd145b083e444d5370feedb610eaa60a7a92c2bccb4b9fd32ac942dead4e9b821f7ba8914fb8a2ad2c21c9275"
                            }
                        ]
                    },
                    "sv-SE": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 45429764,
                                "from": "*",
                                "hashValue": "be01e1c21b1b23ee2bad4e5ee790a197562d6e0f8c50509bb0cd0fd07ef9431e1cce084922db2d901dc3a58c3b79ab723dbd90c88fd02b33adffc6478c4b702e"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 6673577,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "2aa1d6525f181115220cf1737df95dfbd6027ee0431c6aa0e5ae890e38306be99b341b5611c1e4542bc9ad10ebebf9aeebd4808ab8612c98281aba9838a85b0a"
                            },
                            {
                                "filesize": 4805613,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "3e6dd15907bf94a30f3109b8b00e21fe1aa248eef915eb1900ea0acb0c50d8a2ab569ca63ef9ca3698e5007f798f5f5eb14884a9da39c8f114d5f5edc7c73d54"
                            },
                            {
                                "filesize": 6354290,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "12bc0d877e1faa0e30f2a09dfc6a9a5aae9790b96bcc70e674925cdd782f8a8264cb3254f29ffbe0d182fc4ea8a3809106cf8145a64ffc02c3e5a2e4f7590f04"
                            }
                        ]
                    },
                    "ta": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 45107242,
                                "from": "*",
                                "hashValue": "3d9aebe2b8a00854143ee9081e0b569844a3ef1b2268620c26db0068a40fc765753b658cb8616029e95524f177afba7858e8089a1049a10f2d2defce5dc441b3"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 6673609,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "0ed019f655f633000476798babbe109716b3e3ac458ceba17e80defd7f3753b37afa04c37d023e8cc28f6e5003efa92a7f5d34d8f26cb929ac1a7b1fda07e0ce"
                            },
                            {
                                "filesize": 4805633,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "2d91e3859ac9776fbfee24b95aa70cba631fc9e1964f710780aebde73ac60802a339b25cd73e42f8056bb05405458370eba48653e8789fae7546bd017bfa6f4e"
                            },
                            {
                                "filesize": 6354354,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "66447447b2dbbb36ccbaedf766f2202a0a47d94977e247f0e1bbf336842488b3ad8502b3855990d88b24866e76262f3148cfba62a1397543138a8ac5d8119676"
                            }
                        ]
                    },
                    "te": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 44912868,
                                "from": "*",
                                "hashValue": "996421060cd468837284699c3b56e72f21df209faf836c84290768733aed2eb4bcf68d1be502e897b615e3f6d0d732616071fdaed294cff5cc940153d7130855"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 6673609,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "6dd74eea10d75b6771f11c4e0077e36feb287ba6a53141570de5ef835db2ca8c530ebd171d5abae927f7a37970df9be161fce8f1901d30b428568b85055066a4"
                            },
                            {
                                "filesize": 4805641,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "36415f43ebd32de39a750210200a305f319a1b0e9058b49b6a302e1c03e120f2c8920c23ead8cfbe15f4274ac31489eabb8f6ed12385f089207f421fd7bb9dbe"
                            },
                            {
                                "filesize": 6354322,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "808dc450a7f54af4b1dfec7d49d7a25b17215d0427c5675231f825855196248bdfba86372712de23d91d9c0ce924a74bd87d64c105e3da4f2279aa3d5eae2afb"
                            }
                        ]
                    },
                    "th": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 44891976,
                                "from": "*",
                                "hashValue": "c8d31270c4fe21b03d61ce12db5b9c429bc3b698cb5777762125a878253ce246d6dad84b9d19184dd75b58d43c0a5cc6d93a16af0795931e17c5b5b9280a3165"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 6354314,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "443900426b02330210dc5a925516d08d24ce2f199d1800b87ab80c29415851737c64e2e49ae5b2b968027e55af90f7120e0fe440ecdc13dbff65c4476341874d"
                            },
                            {
                                "filesize": 4805621,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "04f27695a97a9c365488fbcdacdac569f455098c940a254fe8a05cf7363358113da89953d476f7fdbc492f24d911d5042aa348c576d84733c35b0b07631e0e6f"
                            },
                            {
                                "filesize": 6673605,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "7336bc70bb041dd247056f71c554d6ee7c239c85d9ef3661146f5b50c84500fc323e02eec5d3885de5b2c0148ba8cbe71eec28825bfdd5c66bfbd0e033bab012"
                            }
                        ]
                    },
                    "tr": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 44889700,
                                "from": "*",
                                "hashValue": "0080bebceee6ef03a529e6ff653544bf03b83995773da38cf1dcd8e55b599623d674fcf5bb6798e50d339e5246f56a33992f80e6d423ee2470126a6b60bd3398"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 6354258,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "2eef19453865d6b8d049c0dce309206b0a1f63aaba11072ac08d63c60552118fbb780605a89d101f97291a2547494da37be59ff893370aa270a60f23c8287180"
                            },
                            {
                                "filesize": 4805573,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "08f9b157c1958bab77f66ad9218268a7e2cec3779de554fe6b44f87f820bd6b8411516d1ce75250c3f454a28a362fce9526eb067815ab351e489b66bf2ac82d5"
                            },
                            {
                                "filesize": 6673541,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "6f5932377a3ab7145eed1ad40da9e07029657be924a439a8c472c0b789f78930299e16195036231a10a0d52e7decdd08d4bf9e981c9bfe946122a0d71d343d10"
                            }
                        ]
                    },
                    "uk": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 45779044,
                                "from": "*",
                                "hashValue": "fa92989d6c659e2d4c03d74b64febc4e497577b442c28b6ab6e5b1aacf3ec3681b648d89908e993a5f2e816cc47afe6745be4e96d953ae21dd78e453b0f565a6"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 6354314,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "21fc6f79853c69845d72fd27cc2df84d0fed9a7ff9874a41c5137bec936e7e66ca00db5d1135c013df15f8cfc01596f5e0155cc12edffa8b28869b224211217c"
                            },
                            {
                                "filesize": 4805633,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "457622b4262c7faf5ce678dd20a5a033dcd6fb1bcc29a4ef9f10f4ba9ba7a03fc16faeebf29dc14efd8828abcad85fd9d84ebaa8eeb1e31e1fc8b206e5cc4296"
                            },
                            {
                                "filesize": 6673605,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "21636608f8e74cb74f47b399f7d3d1391e03d8bec9ac6c203bcb40f4a5d2918fc058c9887fbf57d1074b272ca5e423c6f4b6d8a4094be5e5da5ac2d0d4039c7e"
                            }
                        ]
                    },
                    "ur": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 44904720,
                                "from": "*",
                                "hashValue": "c6ac45e98b3974264b2debae58941ce4a4c3e5e4e4db5ff44735295f9eca72018a4d3c1eaf3c81bf2938318d2e8c22fa633ddb7a7ae0ecf8da405d683b1b137d"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 6354298,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "241a7ff5f8839126dcc4b69d41ce1de7d2f75a939c282dfcf4e288095631ea55b39a33f8ad6894ac8cc9d4a36f2443dc7f17f262a5fc482017b4f38aba9f8496"
                            },
                            {
                                "filesize": 4805613,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "5d1858911c0b851100e7b1bda6daa54ec76ccfd1260a1e8c453d2b91a14f047cd23db013724e6d80f6ed69e36b6c49a17e31861c917c043bc7b5edeb2546a31b"
                            },
                            {
                                "filesize": 6673581,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "1e177b862f3645c0465d470c8190addcfe554bd150125462e3ab712c1d81b1aa4c70140a575e767584ed60e6be99aa9b7ce2d33046c214a4a21cc1839349c0c7"
                            }
                        ]
                    },
                    "uz": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 44890928,
                                "from": "*",
                                "hashValue": "082db9bacbe549e431731f3e88503745776eb13fca8591303ac9a72a49dc7088c85ad0957b3f946a10bcd24bf9e84f2d0e720a55a61fa93007d25591637812fe"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 6354254,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "cbfb8322fc9b5e4a901e504bf5f872b8ef437d37a48ff34873773f467ec0ff4ffc91fd44139ef7e2599128c1c7cd1799953a5da6e913594c87943e39a26a9786"
                            },
                            {
                                "filesize": 4805573,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "be1c79a8a9d3f11c00dad1138a747a9ec9963f2c6c5b38c6e8306549165720fc9e34b124043e5682233a12d1c97619d78b932afdcf9514ce3f25b358273f7d5a"
                            },
                            {
                                "filesize": 6673541,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "1ea1c3edb8a35728cf18bbd6435683e6e523e56071e5be723729d315398c000e53fc7dfdf5a2d168e8af904f91e3a71b39a56d803e7e4bef2ecce0d55dc2de21"
                            }
                        ]
                    },
                    "vi": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 44906004,
                                "from": "*",
                                "hashValue": "1efccadd8ef8761fe510536b057e8d99a821cfe06f9e0f0939838892300fdfea6a60b5cdd693e758fd462dc5df3a7ca870c748d341c38fef5ce74c723a60b02d"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 6354326,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "4d1088d3ce5d5c884ba5721751f6aee4216e9c95c84a9c337ec7cafa808734de85e2a28aa6d660f09cdcb09eb1c6e9fa0dc80fd57e4be9c9582910f7045696bb"
                            },
                            {
                                "filesize": 4805633,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "6f534b8539e66bc49b259dd775f6a5054ed0f5a497ed0676c02d2a4f01f6e0410e0006e7db13709665e86ad7e62f44d6fbd7e0ce856b915c834c422083bae684"
                            },
                            {
                                "filesize": 6673593,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "a068b72de9bca09e0077add0fb78d8679fa7d9531846561e7f75621046c31c8f62f43aba22d897f3bf57324f3c02821e6212b5c9a84fb0e9e1664318b8feca3c"
                            }
                        ]
                    },
                    "xh": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 44898588,
                                "from": "*",
                                "hashValue": "1d42ef020813a178c444c2067fb073a31a56b89a41724ee9a84a47ff8e19b9b31a344c5bd43348228c3e89f96d2128e2b3b964998ea33a1b78ef5f44ca8646de"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 6354258,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "ef23e4072208267e0aa5c3a57d1a31c0c4d99c3879dd380d04690c638ef14e697f8b07375f058cb0545b53dc9a02509fdae8e28afb1d181e5034272788450964"
                            },
                            {
                                "filesize": 4805573,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "af9b5d8175089b88129297ea8a1d5afdb482a0dcbfa0e6cea1f6034c63236a09ad652fe92eec39660524f845ebae54ca099e0a552bd62239b1f97cee07e8ad1e"
                            },
                            {
                                "filesize": 6673545,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "ddef925d1a464413d50591faa334f8976e1df8c798ba03a07d8f340f9d27bd8823f06e18f5f3d7559dd0fafa9ad2bd81255e80ad7b31e71bdc9a2daa504979bd"
                            }
                        ]
                    },
                    "zh-CN": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 44889488,
                                "from": "*",
                                "hashValue": "88bf39cf0ea198712e54a12e515a321fed5c0151b462b7e183d4efc53b9ef296cf75bf35861459988dedce416edb2283df1386f609760a92991702c2cc6d2477"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 6354262,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "00b75e83d0ff251d8cd779db80ee3515fbb53fa54b703c0f514c6b5e60405ac76b3897d99773ee3298b8c0959d30ad56998e6f370b00db2ba88774e79b36289a"
                            },
                            {
                                "filesize": 4805561,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "f92722437b6ac81722843018555f6e2b390cfb8963fd39e0bdb7aebfc44103a18c5f1675009938163c9c3994a790f09236a838bc42fe877a5bc2c015057699b6"
                            },
                            {
                                "filesize": 6673533,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "245965291c4dd9d93d8b763adb6a58755893ea419ccd789232c92ce2daa72d8f969963f602c29f4395f75f13f2a222e9e73e005b940b1575fbda6fe9bf73158a"
                            }
                        ]
                    },
                    "zh-TW": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 45062558,
                                "from": "*",
                                "hashValue": "e9a22b83927f3625d1f68ca4597384bab6e905029fb337de0d416580b73875abecc132e6310143ee41fb42bf17909e26e6756c3fea632019e11de6eb01397e59"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 6358482,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "b6f5c1677fff7e9b59e20f403c7fc30e365d5d6a99a933b76bee9ef7365f673e842396f3bd7bc57dc84e0996374d365817cd485fa1ac97f7ce574f15cee17712"
                            },
                            {
                                "filesize": 4805801,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "c1fb7bb58b25da91e0f13b94157946b91e5fea4c8c8b882d602e569929d232afd9c0f28fbd3d8a3ab4d1cec412f016f854da3e8738c3585d1ef6876adb0a67da"
                            },
                            {
                                "filesize": 6673769,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "6f9a55032cca8143f5f0eef3fe3ea3d9634b98c3d57473e02d81039b88587295f97a435686ac758b1bc68f3f74b691989ea263ab90340d270d58a8232cbbd7ad"
                            }
                        ]
                    }
                }
            },
            "Linux_x86_64-gcc3": {
                "OS_BOUNCER": "linux64",
                "OS_FTP": "linux-x86_64",
                "locales": {
                    "ach": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 42912476,
                                "from": "*",
                                "hashValue": "35bd82244c3b4d1f1b5711977c3b40e1f59c721db1c7de7d4cbd1a8b834f470d8747b3f821ac81b95c2dbd7e094887ee6fbf8b73c4e1e7bc2e874d1c75f91577"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 4596733,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "a4d98c63fd0a2b59c6ac23fbd495fb6c1361eac83e27f482346cb25eb2cfc87c3759f7f68cc34829653aa25a9df638a9cb02eb9037c5f8fc9533096c2e748039"
                            },
                            {
                                "filesize": 6261985,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "023e3d867cb4a667560b12af2de82df18e39f1e2b9dce0f74c27b49d3dfd21e5977ba273b2a843bcb8664f45a8542e0b01572710b7e73a56c206c51b7b49ae27"
                            },
                            {
                                "filesize": 5525185,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "27af0e6abb28c7d6ed4fdd5915712cfacebbe817976a14f7a121f01cc5218bfd38f31137e7de74a6b4e99e2b72638e061702bd39d7bb6f741f9dfac5150ddea0"
                            }
                        ]
                    },
                    "af": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 42912228,
                                "from": "*",
                                "hashValue": "9c7aeae72a0f30caa9a384c289327755de22ec5393f4c7bfe1862d6047cd9dfd0092c82bdb74a435bf9aa1fb8ec9e553995366f1795c7af818da92f4f277f811"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 4596757,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "dc95bca333daa0cc847e7a70c7343253acefa810950f6e24c9b150d2b97b848fa941fd823b39ef3a6ce444743aed4eaa558636b4817ebc59a3670069cd5469a4"
                            },
                            {
                                "filesize": 6262013,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "6712b6e020d3472ced9e2180a2afb95259f7776fb423b2ea22d3b98265bd9d4ec39fc043d4bbe915670d34037eed5157b66bfcec8cae9a4158cfe94585c8b440"
                            },
                            {
                                "filesize": 5525181,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "25c67f5e5bd79de20bdcecb843902b933efe6c998422a06052485e4c4abaa91c7dd28c1f7d7eea5e3bb6ca3c2618edc79ddb2a0de7ac13429ab96e6e49febcf0"
                            }
                        ]
                    },
                    "an": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 42925404,
                                "from": "*",
                                "hashValue": "6cd10ae7c80985500a6eed0a565d325edbb3395c592e785d6fdab93bbb7b998526293f69645e24dba6f7a2f098f00e4292d623c4a292531786efea6c1b3c10ff"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 4596757,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "990c51dc30681d3026dcc9ec5156f310c6e4ae8815f76694a55dab35b277deba40690ff524db7df6cd43d2996d376a6fd1577db51685f7a8e263d105a6a146bf"
                            },
                            {
                                "filesize": 6262013,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "46518409efff9cd44025b01ca272cd4d632e4850aebc735099ea569641439b0dac68faef227a54733661c0aa5ac9fb083a3f031274471c0363d1589a5ac99f9a"
                            },
                            {
                                "filesize": 5525189,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "2b9e35d2528add3d8b4ac1ac57d59d06667abf038ca38a305b2a24329e63402147be2bc7ec09c31579561ff23afbc4f15055b506673e33ff0e2b98906a1e8dc9"
                            }
                        ]
                    },
                    "ar": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 42924300,
                                "from": "*",
                                "hashValue": "21b5731d4f80a83a606245f7ca8f401d296f273f3a10664ca1cd5322412bdd9aa2d6520cf384d5bf402ca95d2e3992da57b0652fe719f3ab543edb0bc0c36bf9"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 4596737,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "dde5dc15f5300ee1c39bbeda08a32313fad1f64848da49846e055458d82b96a086e24d7cb2874315bfcc123368d0fc19a2ba0ec93e6f7ea09312ffc688c3bfc7"
                            },
                            {
                                "filesize": 6261969,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "46104695322c815dc73a44c126ade3a51ce3dcb67d7aa70b1c535ebfba5a5030ec67edb537a582ec84e87387397870118883989ef97223a27b91bdc803a2bec4"
                            },
                            {
                                "filesize": 5525189,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "68a1dc10f9346d3247d1887e3f9163ea42f030217b083fffeb87249871672eeafa33016f5959498824d9b56b055b6854c1fe5b5ad9684ace21c8278f3067555d"
                            }
                        ]
                    },
                    "as": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 42924192,
                                "from": "*",
                                "hashValue": "9ad00c5e49e5e7a11c9cb2ebd6b989f5943a70937eb76c46993b7b764542752077127e5483d042daf6f5fe8a6ef5e953ebc2d00e6a428aeaf0f10f2126fed913"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 4596749,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "6ec522e4087ac082c88f7f3e43c3139f767a295552f314179157078dbfe2a33b3e664a7fd4d185ad36fbafe2c94fab591a5bb5926c38f1111f2a44075d33a89e"
                            },
                            {
                                "filesize": 6261993,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "66f2a4db0f3dae69214e3e1fdf82fbe717f58134dd9f7145e868344566bd0fe391a51e850c5000a2e86da7c7b5efe0b2e56f644f38aa74fdaa6b4b31a8d24468"
                            },
                            {
                                "filesize": 5525213,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "b1516b1d6421e5ffc20920f53501cffcaa6b531e0b86cd96d5fe91cd6048da106c126cd54dc3bcdf5c1ebff11aef1f152a18a049d5af69fb2c2df40a5a14e0d6"
                            }
                        ]
                    },
                    "ast": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 42922260,
                                "from": "*",
                                "hashValue": "99cc7e14d06c488d1801c3a0e54d529305ed3b41a03da95f31ac1ebd38a1fc03417f782406e12685a4b8291c485c6a5144424da2e6372f402b15b3131d11c168"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 4596737,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "b1ff2731c729357b586bf2005ebbb1eae421ae12fefc3383175222013520759c6f01ea6d2ebf1faf622f457676e361a0eda6aed4f0941fb97d3230b8ae57c55c"
                            },
                            {
                                "filesize": 6261981,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "587f998bec07952739a4455caa7f50d11745faca282e50480d2c9d7d91e80db39698b9501e4b53c52900f33d05e128205089398b863af243df8ec5c3a7222347"
                            },
                            {
                                "filesize": 5525181,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "28ed4f38bce3973fa6554744d2907f046414a10721a51f9114f9490a244156de0d4f2162210fb96e7e65d7b5b35d25f5d653f4747108d46f0cfe88d9d0aa09d7"
                            }
                        ]
                    },
                    "az": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 42921336,
                                "from": "*",
                                "hashValue": "6fa15b65f2e35790222ca52d57e9081a09304da470ab4856c75afa22dbd357925f3fbbe84e10660a89b7f3ef99594b6d18957c2bd31c55dd8bc4647a04e92d67"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 4596753,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "809ff9d6e3e91fdc7935a94a7a57e4966959bbba6358a2d3cd2bbe732dbea999330561806652b51a80af2d85c5c101406f928c992ec146a473c877d946bb6f35"
                            },
                            {
                                "filesize": 6261997,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "375ca12c70fa420f696d1182cfc90e81d2d86b8e24417da3707172d363bf211110f5f76db241514d754c79aa50bccb82ea630b47c0623122161a15b044183449"
                            },
                            {
                                "filesize": 5525173,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "b8d5465db1e01c3cbffbc01166644990f08c73ad107d0c9f097508593182f4a8d6bd1c4177f11bf70963a76e34c2d2e00d13f857c64a88c69b43fdee5c259db7"
                            }
                        ]
                    },
                    "be": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 42936012,
                                "from": "*",
                                "hashValue": "7ddae4b8f1fe9daa59369a9bff2d2610d8f7c1b030f576b1cec25b734511e14aa98d0bee99e0354d28cec79a566e6df731bef761377157ed90b030e23ec1d791"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 4596781,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "a5a93c2907186ca47936dc3bc1fcb2ae4596aa21fa1520ec5797d2a36d067760443a625295bc341e6812a6fb494a286b72f52e28489620cd9c0bde3f4f3d11c2"
                            },
                            {
                                "filesize": 6261993,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "a509d12639fd24d3f629a4fa6f21af1e254074874180d6fa85561da228c238136fa4b09a0f0281e0c691713f050e9e6f1f29991ec05426ed1016b4e11fb153d9"
                            },
                            {
                                "filesize": 5525217,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "98da6beb92e928f8d34550dd5696cb309029750928e20f924187cad8d5ce963b96b40494a575e23ca1c3d2e71b1f871cc54b48c6c5dc78f1bf5d7e68fcd7e85a"
                            }
                        ]
                    },
                    "bg": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 43610936,
                                "from": "*",
                                "hashValue": "f01897d8c4a1326d1cb1087e99dfc2db009625ec1fbedfc49f86002c0f156641be6ba7aa6e1017d531f2c806e419b14bf4a7cf61a881d84d9b0c5f5fdeb86a10"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 4596797,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "a258f6e5abc4cf79ed87a8a36f04df705cece3430d8cc48ae1f9579bec57afcfb94c966734a6b3f5852f2d9666e05a4466762335f67e369e70de4376edde623a"
                            },
                            {
                                "filesize": 6262029,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "03001af3576f7a2971161cce6ef3ce9c8419db38181b2c61495d25ed7a58b1a1430f3d12843acddb50140f27133b977967c88f1eb6602f12ba10b5fd656366c8"
                            },
                            {
                                "filesize": 5525241,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "db369f4b352cc32b80d058021440e51e4abf3431ac5f2addc424e3692414530159f50a72521eff1ff667e75e666f4e20e2604e55b0e20a2af3b800befc4fdb7d"
                            }
                        ]
                    },
                    "bn-BD": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 42938460,
                                "from": "*",
                                "hashValue": "c5709820fbad7b25e07d25e063d1d95c15656144ce7d4cd43fd20e63a230dd877a7bfcf7b505dda7956f4e44f8bbc3a2f4a1d73b09c65e30d2956d30245ccb6d"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 4596805,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "9301f1b324eec3901652e7dc394790f736ecd993f08e9a9269a542032d6a0528b18111e2e767286802bf9cb109eedbe1c73aa1fca898e2fdfd9be73580df37ad"
                            },
                            {
                                "filesize": 6262041,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "1826c3d4f2a144be5b08a53003f1c4de45e7087d911d323512966b7ecf084fd018df8b6e64b0f6cbb4546c5f174aad8df3b66aaaaaabfda024507145a7733255"
                            },
                            {
                                "filesize": 5525249,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "3622e9c291091f6ee7bb89e45e8ce50b47a502c1ce2bc6c82aac2c72c5db29223baeb4eb73cbc5db0d66a5f67505010037ab3c502e16690929e99e7225c77270"
                            }
                        ]
                    },
                    "bn-IN": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 42932860,
                                "from": "*",
                                "hashValue": "2196d2270b54cfdd7000244618578dd9b4475124dfd2278c6ba7dbb5ff81ab4619ea9e555c02f7dc38993731b7de95dbf81704afe9a1ad6393a016372db5553e"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 6262073,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "c93a7657203fadf43455015654fd02820b3f2a8a2a59bbd95520a63c7f0cd66dd0b2a1a16c99426f72b2fb81c66093175519b72eb53e31e94c1919a3372af604"
                            },
                            {
                                "filesize": 5525265,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "13fd2619db622b71c87e4ff08a1db90cde01c78c8825cd1be4b1a7eb9941a7fdb8b5176da44a0ba4579a02ac976d698bfa2ad4b9dfaebb5c76b7ae30093f8ea7"
                            },
                            {
                                "filesize": 4596837,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "6aeb41b9fd7d2d53d6312b46a74fc92ea711dd8a7866d7bb4a8fd63df0e84d585d0e4aada53600b181d689a148f353d782c1a295a68a941a8fd5da38134837fa"
                            }
                        ]
                    },
                    "br": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 43632752,
                                "from": "*",
                                "hashValue": "45f4dac7ad2098d695c7b7bccdcdfc53a1384a3caf1b5f32d88651d8511875aaf38909b0b0b64572a4110731f95bfbaff1a576a0fc6aefd887c2e9c6c6c195a6"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 6261997,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "b365f74d8ee64214e59d99ed61ec27b16a4cb017566180fe6bba9825db7083afaa6b9065a1959918f86b8775aedddcdf09882ff93e389d590e93d5185ebe993e"
                            },
                            {
                                "filesize": 5525213,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "40ab6cde629bdb6a27cd6e27aa0bac1c88d04058a84ac80f9b6bd322cdc5ea702c2db8fd464e4489c9fccba369a487e2368b793c0be61819b796d1f4c1b1fb53"
                            },
                            {
                                "filesize": 4596777,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "5f79533b231153f199c41275bd7533863798df7abf0b9e4d3fadb0bf44e21be9666453c12c140c682719ebea89839054c58ce259197e2ce1f8ade16383c2fc77"
                            }
                        ]
                    },
                    "bs": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 42922064,
                                "from": "*",
                                "hashValue": "40994c06eeaef68050d0f1d1b2ffbf6d98585f4853202eb7fcabeb8a6e7f5a5df8eca58162114bffded57a6daeb999680c412b5e4aab58335dc41381cb6b7de7"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 6261969,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "714e9da1f29899a323eae7917821c5cdfea3e1ae586ca06e5f4eb7ce0bf4aab65cbbf70253e0c894cdf1dbc7eddfb83602e492d5afec0dcd767817f16bbc1c06"
                            },
                            {
                                "filesize": 5525201,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "67ca3579028cdd1246c30568f051fc7fbb7f4f61bb335bff71f9b1ec86f94bf18226f9e81cc005a6222c701f03938c2a1de9b7ab19f523f015ae5f2cfa7ff6e6"
                            },
                            {
                                "filesize": 4596741,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "2a7eca3303f8ccce0bae1a3b228a4966755d3565906c80dc199d1c2c57d1c47c7d40d74cb288080b2474600b46517fe28e58b22e7ab5a41024e23dd31659b1af"
                            }
                        ]
                    },
                    "ca": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 43249956,
                                "from": "*",
                                "hashValue": "5ffd8bcee4810766a56016a2cec6ebaa939fd24e9735eee8b86dad4f8408eea9a28388f11dc2171ae2e0ffd84da65b45708430e66a2fd8e6578db4ac43026e9e"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 6262021,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "a9f9e2a463092219b6c9c23e6dae35b9608aa03b09441839730a806c0d25e44b7bc9a29e650cde01f039094d9d276fef51b3e8346ae2dcd015477f0ee5cfe1b3"
                            },
                            {
                                "filesize": 5525217,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "45e00a4357b65567163caa70033c35faa028efa081374bdcec42588d7658384501aac478c6dced0652a7485effa3729df10785afb5157da57a727eb7c42b326b"
                            },
                            {
                                "filesize": 4596773,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "c2f3cf86c02903c5dc5ab23f2377ba600a20836eb8d69b7e99c835bf3d45c0e07bb9b1408bf1a1547e24c208a686990aff8276034358871b86910441dee5d78e"
                            }
                        ]
                    },
                    "cak": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 42928660,
                                "from": "*",
                                "hashValue": "bc949cdc2ebf56fc15e129e7bcae06de3e831cf9cfab1a404c9acca61a8d0a1374e8acf5e8d7e93e6b7425e269c3f0d77fa39c42300353792a7c0eedec1eb80d"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 6261993,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "06ba909846167a2ba796dece5c971cd506ef04dca766ffa8a25958e64ca01cff2d835eb38b042d4d0bd95caeb56ee11835981c80d9a3de77724aa550a3806bc5"
                            },
                            {
                                "filesize": 5525205,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "e70fb1ac411814cb829a1ae2dd0293ffa768be15b35dbe38d7dcb031fc9647d70dfcf1ed6d7223bc0e5d2ae2f61bab3dcb2d382dd689e75da84870ac005a2ca9"
                            },
                            {
                                "filesize": 4596745,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "aa2ef35150cdf1de4b96358c45a41e2efcbdbb9396dc36d755fe605d3622bb3ec261d8f22a9262eb2d3a9e581fc83696099bdd76b55e4ebb0bf473026a542b7c"
                            }
                        ]
                    },
                    "cs": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 42922576,
                                "from": "*",
                                "hashValue": "46a68a5fdc309b19361c42ea1bc48cb6656e3608c1297e8f5d2f6c7e390d3efd7bbc8d97bdcadacc5abd6601b8c1a722ba26536fe9609c4990dada29d48c4949"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 6261973,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "917896af8316409bbcdb2d5e51a625e95584eb23c67d306687bdbc583941d99d82514e9dd9ec8238b18e4d178bf45f1194020e2b7203003eda21b85898890562"
                            },
                            {
                                "filesize": 5525193,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "6f2cd48ad564d690b5421711a5e1dc0df991a64a548eceb525612cf90c6b35cb6de6ea4e8ac1bc23eb4853fac8495ec0e79e04d49948e4e4fb08353c6d68ac25"
                            },
                            {
                                "filesize": 4596745,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "03dc235b2de225925e5301c1e1a5b1b424533e1fd14b6f71376913cb5f1bfa19ee5488c4722b3489c881ae61f75f84fc883fd1b21d3d4db7f61f5a26cec5ca76"
                            }
                        ]
                    },
                    "cy": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 42918836,
                                "from": "*",
                                "hashValue": "dcf5da5b8f6c3c9f3246fc30a5401241020c318a1b1ae797bc4fdcd514e8686465e535919ba453df5a07f33e39c4efda044bca4f6a90432d610bdc4e39cb0d60"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 6261957,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "373b68d65456579e6f7fad79268d6603416cd69105968c38283e79c84cdb04f391970264771b4abff181796aab5c36e8d9ecc5463f77da15d945d682d71bab7a"
                            },
                            {
                                "filesize": 5525189,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "9172cbf0ce15b30fd4b1127984e7f86fecfc7f7d737ad8be403056f8571a4e0f550ad4d9db5231a7ab992efc2d2f1727da290f8611ae37c35a0c7d1239162654"
                            },
                            {
                                "filesize": 4596741,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "0edb46123d9f6ccd843bc646b89177e1911582356007c9868874a8b1b7c67cdce7b06a7418005b3a113ed834dc382e6b6776641363b0af0420855b45fa148a71"
                            }
                        ]
                    },
                    "da": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 43429396,
                                "from": "*",
                                "hashValue": "ae621ddc8c64e6559f7322b8ca8a01807ac66b393bc603ba700958f218da2c1a63f1bc32c32e95ac1f6dbe75091cd5cc5e4be674c01cbdff71dc1fe62f7841ab"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 6262025,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "4fa3bfb1911ec480bc06730c3c5e6d7664e0eb7178d70c0c1516d24d5c2c0bc796e2249b49912e34636d148bcb117490e136f22d8b8c24160cf831f6cba6be2a"
                            },
                            {
                                "filesize": 5525197,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "bac128c3ed52f8421fc855e5ceb071d625fb94bf1f010bfbc8b1f2e8144fb38d31ce84fa416edcc75b49aa406ff760e3b976dd0ea96e650a98772d91983dd5fc"
                            },
                            {
                                "filesize": 4596777,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "21f61340accfdb32330158476f4b211aacae3be8b5c7e22550b41fce903c53b34582a99d3747c0e464ef7857643bb9a53f5e29bec9e85b711ff53c92576cb360"
                            }
                        ]
                    },
                    "de": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 42922452,
                                "from": "*",
                                "hashValue": "92ea89a162cf3680fc3991f51770dc38fdc19ef21f3915d53249ab1f075a4ae2a5cf49135a765bf34f107eae1f49ab4a1947697af78102d1d0a5aaf71de44603"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 6262005,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "6645c7299b259a87d7e0a11b7f21ec1deb0ca169e20c82937d64af9aebba69f21e896d44ba6fea72d3c02d14e6626f1ad5cc811ce2785bd19804c2701ccd665d"
                            },
                            {
                                "filesize": 5525177,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "70117b1ad0a540ded04c577ed703c3f557d48bf5b77052913e38c96126a5a0e853ae52170f255c1546da4e49147b2033891c9139109cf6149d7d8f6ed5d8e46c"
                            },
                            {
                                "filesize": 4596757,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "c179db1e3c3cc8571aa395045a09e607223e1902bdd5d6dc1d90e5b5569636998e7c6beacd074995e0ed56351da0af9a84c6951830c84d690a3edd13e5e77435"
                            }
                        ]
                    },
                    "dsb": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 42927516,
                                "from": "*",
                                "hashValue": "0b5e3579eb2098f27afb9f00c3493d0aa24f5c382066dda7707b19623c10b20da0e357523cd057b6367aa3e12e0253e1d6a0a57ca6f3b88d67a6013157bf6714"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 6262005,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "f9ffd04d533e8a2dce4a7f9fbed0b8619282166a361d0e32b9327203ce9e9f09403778546e3144778934091c2b7d51eb9332cd16d2db1d68606c1c17c3548782"
                            },
                            {
                                "filesize": 5525189,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "bd33bfbbe73d605a9ba29653e510bc929184dbe2cee096ce1b39cb4c6f06a49ac94aea964fbc3f62f5e8ac742c235f8ef823bf9d145832f5bea064ea36cc72ea"
                            },
                            {
                                "filesize": 4596753,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "04fbd7d5b86527c11b0e9fa2037af4b245bdb6769d71e7749cfaf1c168f8bbf371ea48c5c06d79440e052ddefc7916811e912ef301e3100812c92ee5ce1796f0"
                            }
                        ]
                    },
                    "el": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 42940560,
                                "from": "*",
                                "hashValue": "c690828acba26498309d6d08dcf7b8037aadc61dec336adcc82a07cf1b66f81538885c2554239b1a6c0caef8d270b2c2c839165779f79bf1a9e54b1dfee322ce"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 6262005,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "d272e14955cdadfa84ee09bc9e1365461bd5a41ff19e396e36d0051d23299f55c353f852c44138579a79aa7d383910174d4c18a850d39fe92317d86d141060d2"
                            },
                            {
                                "filesize": 5525221,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "47e7059595ce1b0d2d2f983071281bb529d9adfc4af8a6312be02f3251c22b50a7e66880bce00441b0aa7a249e2f64f158743a20df2fc97d3b180a1a9539223e"
                            },
                            {
                                "filesize": 4596781,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "f2ccb38fda021d1e7717389a715eaa09cea216cc55c7ce1d1f8b62af2564d1aa8f62c2a755aeb079cdd1b3187a5ef4b824bfc55b075b54618b3bb1fe74527970"
                            }
                        ]
                    },
                    "en-GB": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 42899892,
                                "from": "*",
                                "hashValue": "1a64fd23b8e9982200483edf10d0b846196a46749394459634a801e2ecc9e743bd6cb3c83fca3e34bd06c0e8634d715cb7634706aaa42d55d37d151d2ed7224e"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 6262101,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "c04049381510f63d8aaa9abeed31a9fde5f5d2c2473781f0f6f25a5d5cff7621c984347bb87ad94467f4d5d45fc9d85475d11ba3c2049c3f9d9fee88a3fd2d83"
                            },
                            {
                                "filesize": 5528765,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "35f4cc2b215e5d498cfbc17bb8b5aa8d1ab2af5c93452eb2bc996448c8a8e80e2c4d6465996c402eda4a56539e27ce8f7e12d2007e7738c013035895c9433468"
                            },
                            {
                                "filesize": 4596857,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "488ed8075a913f1cca545af6fb675c9e85ec77f40215b56a15083d0688e57a6e1bfcfcea20fe0d860fddbb6252f615721ee6b366f55052b6d67216e94302f520"
                            }
                        ]
                    },
                    "en-US": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 43063790,
                                "from": "*",
                                "hashValue": "4c79cf94cf97ef00a931b27e26cd67ca33e8de8968875e478affb3d111650d749868949335642085d5833eb5ff166d314f881fe1f7a05504f0e8d593fa2f1396"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 4596821,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "f36c8307dcbb6f74a5954c4d1910f42e2390e2701507d815d9e1f242f6b0c420ad6d7c613d1b1c7ac2768a5442a76739a2b4acc264119d1f4aae649c864988bb"
                            },
                            {
                                "filesize": 6262057,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "eb8248a104a713f70e1882521506173f1ca493fe6c8ac95ef1b476cb07035ad368e4d4c10374587ce1aaf0eaaf5d256b2520e0cae9b8fe8151aecf1831975dd3"
                            },
                            {
                                "filesize": 5525225,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "7f8362c02e3835f98cffa8a448e1ddcfd43c177aa479d4a5052d5bd789ff17b22eb599360b5e5a558599b56c1a9ed308b3dc1b1171cf2666adc0acb43ef3a4cc"
                            }
                        ]
                    },
                    "en-ZA": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 42899184,
                                "from": "*",
                                "hashValue": "68356a66b501709b13f503a5e1a77bc5b04b9cc59fa51d255963f55784b90c747b6b387d1ae5c030f8bc4b9e8bd3f24586bcf223dd8d2ca1abf1013b9027c5fc"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 6262009,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "a69a228ee20132cc4e8c5b752dec5d1355798f8ef42775232d2aa58c53ac7ed8779c9dab8c2328919be82e3b808519ca8202cbaec192ad2a6f44ca6a19de15b6"
                            },
                            {
                                "filesize": 5525205,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "344e288f3ce2338526f2646307790c7d09c53be2448949e55092e3883aca22d26cd28ad73c8d093ff240b59109e14aac4052dd5cf04a26ae1d1cfff79546a387"
                            },
                            {
                                "filesize": 4596745,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "066d0dcd54ca84ca336d831c54827a3c3fb22134633af212451a7382bc43fa56e6a4f6b03c40cdc096ffdb8078e7ac2863b05c61c1090674bf1a6f576129cab4"
                            }
                        ]
                    },
                    "eo": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 42917824,
                                "from": "*",
                                "hashValue": "a9388a0543685290649374d690dcfceb1f69b14906d8ce169bcb75f4499c270a7bc528b6d153b24e08bffd060e6adc7a80f619b4b3b9b986b28f8221d98231a2"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 6261997,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "07b38fbe3d253d320a50fd49577203b729481345f49d34d55fc57db582563dfda066b94ca5ba3e14536ba240c9db017d888ebe7f7fbab83b66bf3897322ed37f"
                            },
                            {
                                "filesize": 5525185,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "1b398d313a75ce87a6ed34a4d5987278e8f0851145eb6f291b6e508d1157f2b72aca45c59673941735e2875c102b1588d97becf986485e1c8068a1c968c53363"
                            },
                            {
                                "filesize": 4596745,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "957aebb577479a4235c82db0a1abcace8c1995b7e930af5dea2fa5babab9880ba202fd656dd3becdb7afd3936754ed8746b1b80495c311bc1e6ee1f15f7f9222"
                            }
                        ]
                    },
                    "es-AR": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 42922468,
                                "from": "*",
                                "hashValue": "68722c114f367852f930204aae914a3ba6197627061d519179f556374cfa61b778df9deb6b13f43bea62b9713d83bd76535f6f6620ab0c941abb113764f86a64"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 6262017,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "49996188a1ad40bb6108ad4c3eb7c842b2db9304fdadfabcc14a5c22de22ae345d4365fe5dcd1b2c0884ba76fccf70c3ca0487b3aefb717fedd46bdd555b6920"
                            },
                            {
                                "filesize": 5525205,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "2a148693195f2b9a07cabd36463b7fd0d8f7249daac569d4a17414acbe3409e1f7376c9f69dbc4ee5d134d4ee320cfa7cab79efc346b4ad7ea1ae4e15efb7938"
                            },
                            {
                                "filesize": 4596773,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "acee798b6e282659d7f8415e58a01eeb198dfc199ecf299966752185f490d99cf31b596f0cb80e78ed1a6beb6a92887a542a690245d597497782efb09c71b4cc"
                            }
                        ]
                    },
                    "es-CL": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 42924160,
                                "from": "*",
                                "hashValue": "cc848d22ee595305f09ad7963d46b631ec04c6adbad16e1a463def8717bd516a8b49d299172d207893204c8c4ab2f2eec1e3d39a1e0e10c23d74f6a8aa9c683d"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 6262005,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "a13c802890295ad01126e7bf9ac67a4748aeb80a2745290fa75725e0d329aab0dd5860b223ca24d77eda4db9e9699042c20b1f897286f7dc966654fe93e8c48e"
                            },
                            {
                                "filesize": 5525197,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "02bf5926f99b41cb423e1d0355853dd9b2b40e9ba1530fa6d2459e384bce0f5607e07979e3e5873cdde70813b71cf383cc275a2e38df60ba73671e0f24d10218"
                            },
                            {
                                "filesize": 4596757,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "2e333150aca29121165d0ce8d68bcad7dcc8a3dc1b91af2fffe71d64d6a2573aceacb44a4ada5a4425edb09989d475dfdf01e4fe6bb63023f16565681cdf6f5f"
                            }
                        ]
                    },
                    "es-ES": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 42848444,
                                "from": "*",
                                "hashValue": "91de9db2995def2390c218e908ac07aba3ddbb547a0b808afe2c4156c8d9f460022ff1473499e53f3de37474cb66e0e5a2759ff6cda78cc2bfc754d7a1ee504c"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 6261973,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "c32ccd06a6890da4c08f19450d69f36260ce08fb186e146c5c73e3084452ba9e55695ae10988a88a64883cb443c6f9e321de1fec3b7a949d55b5005d4fc802b2"
                            },
                            {
                                "filesize": 5525149,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "2bf2780eb5447919498febbac32f8f675b3c2978fe5955ed7df1d297286c11180fa5ae1ae9f35b34c66ac34a57c5aaf3a0507fd00867072beed8224adbff9ed2"
                            },
                            {
                                "filesize": 4596729,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "97b22c5ad3754625e8150d68ca5185ea9d8fda1b0671a316a5e383054a011a79873a4f339c4ac92770a5e826c05dae90fe38ad4647438ee1d12ab73187dc9449"
                            }
                        ]
                    },
                    "es-MX": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 42924452,
                                "from": "*",
                                "hashValue": "c09fec5062d13ad8573e08468b2d67b0dc9039cbd6190117c50f7e52ae5aa95e9d6ef6d1ec040cdd4272b0c34b568898733b3afbb03d5136541c1a8a02f028ec"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 6262021,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "ef459015bf4d163d95ed1203ffd34caf5aa79e345d0fc7b3c57f78a4275cb4c06e7bff6068f67cab51661372b0198c778b882a9f93a87f8fc6838476e1a0e2d1"
                            },
                            {
                                "filesize": 5525213,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "7acf2dc4199dc9e137e9ed42d05ad04103496c241eab5622ede33f102d9e80910b4b50e6e47616088e424849c82159e37bb741e1658d4a7470a3e400a1a18322"
                            },
                            {
                                "filesize": 4596773,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "a343aa896ec2246849f286e9c645452d41a8dc5bcae013977e8a4dbf44fa99005a40aaf5768566f40d93c8334f27516039dcf228025989810c9fa88e3b9aa31c"
                            }
                        ]
                    },
                    "et": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 43545984,
                                "from": "*",
                                "hashValue": "94135868c9762a61c8a5a32189c56a952654af1f5f78419923d34df352430f371a723b2f56b49f4c8afe806deb0018536bd7544e7617ba9a81634a8e8c764412"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 6261973,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "39a099bd5de14f2fae423660c7df9909958b32fbd7c6cc8ca6f085cdc6b55b165e34d95f82cb18a5395abceb0ec4e96f45e45b45f09ff31d8e6f734ef3b9b5e8"
                            },
                            {
                                "filesize": 5525209,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "2976993f9bd9188679b42c5f5483a5155ccf261b3dcbbc2178997c7736d4e38c7c54b45be172c187e5563c8546458a82230e6d3756465bbf0ecb6c8754b9db2d"
                            },
                            {
                                "filesize": 4596753,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "fe9a34e5b6468c49706794ba844ec7538f17255caeae80bf9cbac7a0f2f0d916cf8e5e34ebc5b177c21395b3e68de1bb0823e97dfaf518f5301e642e2d933037"
                            }
                        ]
                    },
                    "eu": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 42919076,
                                "from": "*",
                                "hashValue": "dfcf5d5f71da970e33b706f3075e150ac2493bec6ccb21bb89bd439f432349156f136c7604c50da6468d43a6e653e128a6b5e32a2a11d438df0e30d279a32e46"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 6261993,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "722e04a669aeca65536d64eb9328f632858d98ee3d1ca63da03d9c3f6410d7d7f089680f9be0edc8343d674e3ee739557d881f7407b288bdcbddec020e753b3a"
                            },
                            {
                                "filesize": 5525189,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "7a22bffcc85c067588b46fd04440674171b5783f75bf4679dc658173951a531746c42dfdc1e68ae0dd9c2d99e954131000bc7cb8ab97db24f85bc115f1b5b950"
                            },
                            {
                                "filesize": 4596745,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "88f1769efcd9c745dc12a38305d4e94d4be214bee87153184391769a54153f3986ced3f85bd546e03549431080602ca6d72f4b89c7de0e4383d9b748c840a3eb"
                            }
                        ]
                    },
                    "fa": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 42935620,
                                "from": "*",
                                "hashValue": "53167570b7a81bf70b3ed5f28753f6ae3f652e727da32bd3c263794152e6a4909bc591f2970bd8e55d7a6b99716d37d5236241d36ebbd0130a7f163bf409646b"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 6262009,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "d5eef4d356d6fbcdbb62e0db16bc0fad77b6d49f7c8349826197b43fad75538c8a1a38616fa7fe2e21101c018eede8bb0618e688681bc1ff0d325c85f7b03073"
                            },
                            {
                                "filesize": 4596769,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "2e2e76d84aadd4c75cd67a0b9f48ec3a109e09cfc8f37f47015cd3c2965164d07df83c3869344f87916af3af13cc6836f3cd4cbf87d3207824248a7b6f379ca2"
                            },
                            {
                                "filesize": 5525209,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "98918fe20bdc4bedebe7e388d1e71a5acb4dbd34f350bf50aef8b744e1171f7f050ff596e8b05e4d75e697518563b01768fb2e38d84ef2f4615dd63aed150f2b"
                            }
                        ]
                    },
                    "ff": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 42921264,
                                "from": "*",
                                "hashValue": "acf96647a6dc2a82a98410115c14b6df1b2376fa7a4f67d22988a91f0bcb76f779ad2c6879cdb579b24ac7cb7dc50896fbbf59a1efa75df6fbeb5fb87e042659"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 6261997,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "8e3aa46a1a2641f97dfc9f21234b67e64ea497dca5aaa25fb5b452f20d8c44a8002b663d84668db582e9e896862825362eff2c248df2d74990c977228773c76e"
                            },
                            {
                                "filesize": 4596753,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "ae0d8028e742e7d41d4400c44988b88358762948478f88d82d661e588a15ca971217e80411b8412aabc60e490774299fb101cecd41885d5c8c5ab7f516a48dda"
                            },
                            {
                                "filesize": 5525193,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "86aefcbbb2d1a3dab83e84bc27db3f5f789114c259aa8504a23955d8238b695f8063277d3ac5605e7d8b44349f8edf7aa9281456a2b64ca1c8d4c5e91e72b4e0"
                            }
                        ]
                    },
                    "fi": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 42914108,
                                "from": "*",
                                "hashValue": "3e6f6ef29f9a990802b728965a533869b943917abf122443f9e9b15305c32ea92650c9ae7fd478b03bfa74428abf59b029ef30131b6edbf72d004e6d619718e1"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 6261989,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "e6149fc72afcf571798cf68eff78f16e5f6143de786a2b3f11279faad96f11187ff8951fa29617abe2d1036e53b93cbf6f84050e0dbefd4f8e3c9ed71991698d"
                            },
                            {
                                "filesize": 4596741,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "72302cd63c875a7de360caf7865b91fa59edaf40cf9331fa07618277d50b7f79c46054561d92f3b05e2783d0181d4e3ed6a70e77dc56ca251444132663c4a220"
                            },
                            {
                                "filesize": 5525181,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "9ba2f25d9b44d3799bdeb1276431ab19456d1d29a01bdae4f09a3d2cbbcf75f1c669dfd6838fddca99869eece8c91f0134bb059db21cbe320789917f70e9bd03"
                            }
                        ]
                    },
                    "fr": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 43209156,
                                "from": "*",
                                "hashValue": "553c30fdf795fb2ef7d149070658b266e98224a10d07af222936304b8867718ad4682b43254d48b38ea15922cff5fb7679f8ef43d2928a99dc7a4411b6cc257b"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 6262021,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "d085d7544ec59e61a2919633ccfb0463551a4b17c4e3fd97ce6f39bb8ac233069cf7185828672a7435aa3a1d2d83bbefece0aae8e78b9a134501712237b7d6b0"
                            },
                            {
                                "filesize": 4596769,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "311751e1fa2c8036c71e46b6e6ea1e354f448d598665fe6f7ecfb151e4f5ffb615fa724276bc30d80aa6ff32a1af337bc234ee0532ade893db7b69076a6aee9b"
                            },
                            {
                                "filesize": 5525205,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "04d75cd5ece9088c9b0f1e3e4cf24d9ab170aef96e6655f1c26841b3f82976409ecc2bacb93bfe93b584f88d6f23d8681c20cd4aa649a741371e87cee3eaffc9"
                            }
                        ]
                    },
                    "fy-NL": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 44210842,
                                "from": "*",
                                "hashValue": "e589303d59aa17535f781f4bee2b199f2f598f778ef10671fb09a9ffa57ac10dae233b1e4578bcf3cfcac6c29c50571ccc2f2690917c98460914c6b7b71fc582"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 6262033,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "9fc2006c0545d774109d9c758ccbe89207786551cdb262536cadf36b233b1fb16efe8225b40d43f1798515deab5d24c96c70ac4cade210143e5be09391445177"
                            },
                            {
                                "filesize": 4596785,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "44fb46726d7c2b85d3dc5e818c35637b3990f6aa4fa41f5c0bf67d666b5a850ad9b431f2bd544aa8dd6c413cb5f08ae256058f21ab2f1894ff89b3f78669379d"
                            },
                            {
                                "filesize": 5525221,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "0ddee55e957c6baf4ae2ca6e2c11daa0359bda956ee88526265bfeeb8b0f5b31f6e599433352febe52323ce1e1003b16f797b2e045c802d98456cc1e60353d27"
                            }
                        ]
                    },
                    "ga-IE": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 42927820,
                                "from": "*",
                                "hashValue": "d1967899adeda004a22f6bf7dbc814700ccb6f3ce9f4d7d0eb7affd0458ffbd741709895fa457a21b0408ff41f20f53ba8c0fc62e8253b1060d3536c8e008cfe"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 6261985,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "8ad871a3beaa1da8b74b21be70e7f0f7edb777aabe5a79798ff8b3e77c2fbf5799cd7f7d83a56866ac4c7e7f0f4bb209eebd6192c0617c01dbd9ef9f35c87c78"
                            },
                            {
                                "filesize": 4596757,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "8deb1c6ff74b49ffe47cdf0d4f414bee7c74b3aec4dd1e7a69f16bb01cf1992d2030e95d389bd52434fdefd144597bd0eafd6056377c9d4bc13b42ad1ca361af"
                            },
                            {
                                "filesize": 5525193,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "569083944c0e0106c35aaa56dc11c2a4486443874aa6e3f7dcf7924baeb36f3c3a0d23415eef384a89d5cf41b57b6386b541abc7f052850fd2530658cee85781"
                            }
                        ]
                    },
                    "gd": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 42919692,
                                "from": "*",
                                "hashValue": "e1370bcd217d0602da24a6f3dd9f1346a736269d687cba9bb9c1b21301f459e9ae5e295c90c32dffb5ef565569acb2c5d3d6568dd6657f2a118d389ca7618834"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 6261973,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "c22f4ae4a9d017fde11b96965d8f970c9d7ace45e5f3784c71aff54624693934725976a124459bb09e62c05e6ce7f1cfe22084d5882faa3e7b72b87164d2ea1b"
                            },
                            {
                                "filesize": 4596737,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "9e34b8a85fdba16f0ba87a564a1dc2585ec4966c1d9e18c3e7696650510bfbec4f65530b9df4e658bfd6f754fc6537f8cf182c911afe3a59fa70bd6c1a72c06f"
                            },
                            {
                                "filesize": 5525181,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "e149d3792d29cecd6ff8ce36ffc01eb6ffede52ee7136a59f578960ca832480511b2b693df98e1ab99fddc5551e28d2c038de302a1aea04671f1983a54cc6c83"
                            }
                        ]
                    },
                    "gl": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 42913892,
                                "from": "*",
                                "hashValue": "17e771376be3a0a9f9ed78661bf1e6ecf667c004f7a156cd049016394400339d66d3787ce74497a47323b4d30c959234395dc7647bf401ad74087d48939b4977"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 6261989,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "9d061e31684ad4d311264b20e4c48d66ba5bc5d367bf969dd65580242244e40501902836808c33ce26eadadc48a62ae452ed157c139c34200886befb6cd59e28"
                            },
                            {
                                "filesize": 4596773,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "d3e1037dcf20cd3c9ad4de54efef3a37696c7bba2e66096a749a279d5e6481347ef02077d073a1b1afd91019b76cfd256b196bf67acf197921325d7d52202dd4"
                            },
                            {
                                "filesize": 5525205,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "1366a1ed71ab5a6b6cf6e182546bf3f4df0e7eeb1b1add3308492cebe4914a2fbc61c9941a18d14803003fb04b28febae68f76a567c6ffd5a9c7bdf33bf5f379"
                            }
                        ]
                    },
                    "gn": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 42925676,
                                "from": "*",
                                "hashValue": "10d137b63d4d8f49e26c562c4e75468780317a9257a4d5b64300823c28c72a4a3acf3f08ac711fa3017ed3226a21ef67bc267c72d247e67701b315696c626c7c"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 6262009,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "8a56734cf9a284b07012825ef3c45fcf90371504be095290acfbea121945e39d942f8699e788d29b7de533d19f5b727d94c6e53dabd625c07029d1356612c884"
                            },
                            {
                                "filesize": 4596769,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "f211ccee82db06e701e5bbaa2ed0c0f1e00756599500f4302e79975e1cf7a9df97be9d3735c6a36ede5c1d794844dc62ae00b1cdc36d831c81ab98473d85450b"
                            },
                            {
                                "filesize": 5525193,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "3e48a7fb9064e1535fed0d6ca2f94e7a24681af8f156c2cb99a60ec6d9433c84a9e0021e0f95635a034260d8190c8a826f35de93f5d023da96bd6d769b51797f"
                            }
                        ]
                    },
                    "gu-IN": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 42932532,
                                "from": "*",
                                "hashValue": "3122d99d22e9b34d3c369e3a201056ab2700deb8d2814517e65853a731ac83623587830d1d25059e3bfcb3b74e13a8e6490a3fa36656d5da9c6bb9a18ffc50fe"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 6262029,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "038b008a0ab021edd445d7c0d7d49e1a6f8803c0d86dd425eb05bbcece12f284f20a344f401cfa81693a18699a1c3d3409dff87de63b643f6aa216fdb4b5daf6"
                            },
                            {
                                "filesize": 4596801,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "dea7f2e95debaa7b88d4ddd2af97e3ade6118c803c7c6caf5f93b1e583ae2995b7a6f32669ce325c76dad3f7450277f6cdd9c50dcd66618d6bb74a5a533f3ed0"
                            },
                            {
                                "filesize": 5525237,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "a2c8cc67cca372a04ba8cf8ea41249fd97afc26e995243d9c2da80a295e48dab5d37a1e9c6452cf7ed176abc4c2309b0fa2ccbb793f07539e5de6a845da9aa21"
                            }
                        ]
                    },
                    "he": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 42917648,
                                "from": "*",
                                "hashValue": "9e73125ee610ee07d042b2cc8379def4ecc92692d5f69c3cb4e2299136298bb91e4c3b40fb4830e48e664994801cefb82b099124b4e4312990057473e9014a9b"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 6261969,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "1069b644da933f11fe6563705022ea75c49b4e52e324f633b15cdac97b99277b866aa052683969af07a3b72f27e3f739c344b502564d4949c4a13a8261b320f3"
                            },
                            {
                                "filesize": 5525189,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "3dd687d3f6696eafcca28928bc866fc7c9c273cd8522f915dea1212b9051bab37b6c45f67bf738b871267185baae0747b0c6ba11b419265d5a313247d8617961"
                            },
                            {
                                "filesize": 4596741,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "1700a50169e48b18571db5756fb470c2997a33611cf32dc1a431f4a633ea7fcbc3732800b18c35385def4c1492ad506e5e720133051e25ca63b5f6f8e21ad415"
                            }
                        ]
                    },
                    "hi-IN": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 42939096,
                                "from": "*",
                                "hashValue": "13bbc92ec9e75fa5541563728ab1360f49c2270a5a562153f147bc1936c559f5653f895f1a4078ee9a84a0aaa628dfd266c58bfba1e244aa38088227a3f4a952"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 6262041,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "a353154916bcaef36248db9304baa847f06b7c5a3f884deab546fc94b6254a609a22531101d15c780e51c3e867ff224fb1506d2d8fb0718d494d029acd108f3f"
                            },
                            {
                                "filesize": 5525253,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "c46323f7b70bbd266e31d02a1d6acb94806319cecca170ab24f9b9266fd493f8aec3787061eadefffc1afd47adf66b479a4933b35992cff07144ed99869c85d6"
                            },
                            {
                                "filesize": 4596805,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "a0df5056871cde2acd78cc32740b955b4dff1218934eb59c26e0e67cd10718c85160c8a18db44d086e8ab86b62cae455ded955526595e62092bc89bf9b6f049a"
                            }
                        ]
                    },
                    "hr": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 42922996,
                                "from": "*",
                                "hashValue": "2d4f59b3ff5d61a6c9fd5b6a1afafd28f5241d31f4eeed895073decf2a70ffecf48f0c10781ab5bb16fac91953427e55192c38ae728bccd01325f0a0dd8fd5fd"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 6262005,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "86de3430f12eec8e5afc7b7880ac90fa954cf1226544868f3007e4a3d5c7897ff732cd623b2f4b6d6af1a46040e122fd6dbad852f53fc8e665cad8a80f920daf"
                            },
                            {
                                "filesize": 5525177,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "5509c21551fba659c05a5dec5438d023dc76c809114b4aeb461c04c8ad0b23ed90623852da43995b0475db8fe894fa41d9cc659f80cd66fe7334421e8b1b74f9"
                            },
                            {
                                "filesize": 4596749,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "f6cbd5b98bf5f22b9ad4d21014833e20a4775c8b88e17242af2412df15156c55d0ae1701ef5842e680ae609daa3e9055a67cb7b98f8341d290fa2f5c4a03b7c4"
                            }
                        ]
                    },
                    "hsb": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 42927448,
                                "from": "*",
                                "hashValue": "995de3b6c170c12a576844be7172c710385aae2928f34a3b8bedc6c41144fe50c0492b68d804f26b5fe35964800eb8bf3dadb20866f73e59a33f34396ed2d3a1"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 6262001,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "7a8b5d3c0e3b2538b60affb0c253e20bff0cc6268865c5ae7d9907c74fbd9ee91c118d8a3a772548448ccdca7b77840ae8298f5aa90f75eb5c7a6dee591626d5"
                            },
                            {
                                "filesize": 5525193,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "515ab044cf37350c46f3835329e5c049c5b98f8cfa171e50e95403408b4316e0238907f32b2f3500d69eea4c81416b7abe3118bc8a31c757d3f9831800b43039"
                            },
                            {
                                "filesize": 4596753,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "cc8614ea4907eafccc2de50a384f62dd484e3d7cccecb297d401643a446df376358369fde890f2212df5ee8f5f52b81cca046823666a50576c3edf3ae2707fca"
                            }
                        ]
                    },
                    "hu": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 43479616,
                                "from": "*",
                                "hashValue": "fb11d2936d6afff7e81e78802c7413c3afbcfd8633966e46d7df76213a4761d5e02c38dcfdc6d2bcea1da70910c96904e706df1626efcb5d24ae5196ef0efcac"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 6261969,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "d3ca1424f71669f98b36496ef497d2e19b154fd81df2dce58ae0cdc8217fac549aeebf690295abba259f99215f2cbcc938cb51ce3ece94c4edb49543671bc7a1"
                            },
                            {
                                "filesize": 5525217,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "156557bdd06c1c037cd776301ca8052ba054ea898ad5a8eccd938604dededaf1028136a51607c9111971b667b85f44a6afbf52e5924043313c7b2a81bf1ab5ef"
                            },
                            {
                                "filesize": 4596745,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "2c5bd512fd2baa057f231a27cb8ef705e8cdd76cacbd9ee3a19f7f6c0599abb150ae02e3bb1781cfdc6be6d4732b5b0d8d8190091da60973ff07a70518530061"
                            }
                        ]
                    },
                    "hy-AM": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 42934188,
                                "from": "*",
                                "hashValue": "713f471e45e790493a0e15e3ca84cb398be53e53114969344164f9e3be66d6c5fd0311d85e87ac95037b5d44140d7b1a9a537d8315153cdfaf9f27f778fd5056"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 6262013,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "e7a34ec332ee1ea25dfeb63314aac1e93c2c2f86911a29ca62a6c78637d75b17d7d30eb68cead6a38eb9edc240abdc55c23186cbb4c480f6a1decc15419a6f75"
                            },
                            {
                                "filesize": 5525229,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "0fad421f50e4a3c75170739607c4aa3cbe7c20d33b2b7e0c8cfaef1217cf8262e1de07215de1c5fcd2b435347c0f5e8f6fccc63bbdb5a11d514072f6226e2014"
                            },
                            {
                                "filesize": 4596785,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "81d2ce651923c900f012bb19e7eed936bb5bcb090de3bafa2be153fae9d224a11226c0775d33f33408dd553f029ebc23a510c64730589ba4d2cec9368fad95c1"
                            }
                        ]
                    },
                    "id": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 43007228,
                                "from": "*",
                                "hashValue": "cd01ed3d5c3ddab08974ba065e2e40af34b9eeed3ecadae8e4cd4edd30d57d35f6a681c1c89e4b979a13278ad53f980b4ad211cabc435a39aad1d31af28ecbac"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 6261973,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "520cc2071a7b5b4d53ad7c816be1f40bc29fddfd4fbdfcd9bdea674eb8492e803a812ad93a7501b59b1c94fab1983dd5d9e92bca2346329dd181a69e1b8f0130"
                            },
                            {
                                "filesize": 5525209,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "feb752a43629552a1d98e910615bf225836ef05f6171fd02cce74d9181fd2e7889d917c2148d89ba9f58da17a37e34427c0181a206ddd05e7289c85be785c829"
                            },
                            {
                                "filesize": 4596745,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "fa49c86c36bd624117abd453dda087f42ff575d34745b66238c62423aa87d0e193d6134bcd86aa695b98e965e89c00a29888bea53a067f241e420a41af4d6d68"
                            }
                        ]
                    },
                    "is": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 42916196,
                                "from": "*",
                                "hashValue": "b3a31c28831ec13efc63b003f27dd0f6257bdf981e8ad2d19c778c54ca5b5ab6abb2e9b99d4729cb84c206964eba5f91df1f22e5a4f15db4818ce2258935fc48"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 6261989,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "dba472a17dc36c844aa70cd75b8cb2d846bca36534d319ba30714b4f75c2d38ee55425a58839d1aaf6c1abbdd5913328feb01fbbcc8651651d4bbf105c5ad17d"
                            },
                            {
                                "filesize": 5525189,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "58333f3b6478e6f3171b49ee4d0fa228e43ac34651dac27300cf8be2967ccc14c0be75f80a2767d18a17cea2290eb460851d78b441d9e62be636968dcd31130f"
                            },
                            {
                                "filesize": 4596741,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "8bf62391ad7fc99fc69711938cd7706acfa27f73050b9b384ceb062daf3deefee97dc5d3e6d85290ddc8fac8a49b0efbb3380efa43c8ac3244d8215d6a5592af"
                            }
                        ]
                    },
                    "it": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 42842832,
                                "from": "*",
                                "hashValue": "878c9850abf98e6366c23c24f4793b675896ceb0afd152d79c1021c3abcdd02d10dce3591d9e63c1f826248dfe7607d2f65f75cd70af3bb5301e5a27a6479ff4"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 6261929,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "f46c25b0fcd3bc8cf9ed10e0eb78ff6f4ec93b33ace8bc026d04362bb4c20afc0cc62384c43f2cf49a9a3ed3a9448257226333bcfa3154e80d53d70fd5f644d9"
                            },
                            {
                                "filesize": 5525129,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "ca29e024902a7e1b766ebcd30dd23d6668c0b401c066af9dd09680ae7194b93e0dbff3aabee37c664b4f84582410c884dd04b8d7d85defca157c0fa525dfe977"
                            },
                            {
                                "filesize": 4596697,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "d4d6408f21178f4f1885c5d07bfb24d41f7ad8d6f075c36568ff3f7c73d614ebb8d9b76b920380c75d6e1b1bf923ed5d409df8838be1336eb01c24b2c30d2010"
                            }
                        ]
                    },
                    "ja": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 43108330,
                                "from": "*",
                                "hashValue": "623feaa1182ac17266d9c3e65cca625aac86f81979256dc60431e75a59b5ac10e95b4dff9ad4d09df56a4747c849165d2777073ec516373fab6939f15d8271f9"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 6262049,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "308b097d8685c7b71b04642644765a73e8d50b525e687cc77ddd3a98162af13b428632dbc50ee5a9ec701c3e3786d5a5f6819a5111e5e09ebd86c252dc10392d"
                            },
                            {
                                "filesize": 4596801,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "53937a0b7251ff32e4a172c88d0ca76d709b1652496845f46f42744cc3d6c9d4495afe8cda116e0c80be0184cbf0167b06fb8b3fac6bad6a9aab9e4a2bad7bba"
                            },
                            {
                                "filesize": 5525245,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "bb77b56e1c929b99abc07f0c1615cf961a8f3fd2fb39493706c62a35b41b13be094417665c12603ac9da19f3ce61730dbba5b32b9614c792a949dafce2307347"
                            }
                        ]
                    },
                    "ka": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 43109288,
                                "from": "*",
                                "hashValue": "162b9ba529127ebae4f2abadf4afe19dbad58be6c0222613206617d19e4b859c801e6ff25f9f9ffb1255a7f6712413539812a948e947fdfd165bb5de8da572b1"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 6262057,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "51f7ddab7673af3cb3cb9665a8a328c423cabf1a022b1d24e793631c8a66403c2dbf0fa07bb06e800b8ee80435fc04099de6100be406f1894991548b2172e8f8"
                            },
                            {
                                "filesize": 4596813,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "cf5c00c4d95b7e2edbd7b535c7a40ae78a3b4d9bf3f9548916a0052f5fc69fe5463054f68b08994958bb5763869fa51b306ac8b34af2383d858b5286651426d5"
                            },
                            {
                                "filesize": 5525261,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "0e892075292f5c782c26a34c5bfa27b2d2d495ac5a6bc866369224484f44a6bbdc46b2ac2870bf5878485cb3a8f270259d2245a31b701cbb0bca7915cb2c3958"
                            }
                        ]
                    },
                    "kab": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 42923020,
                                "from": "*",
                                "hashValue": "c50e8eff2427ca9bbca526e21dce04013cb31ce8eb652757aceb66445f8594a6834061ed2bec55e679ea7f13807780008970731363968e3b5794c114a0cedfe2"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 6262025,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "119d61c92628e07e9abdc7e1bc24146b61fe05f7e5ffc9f376e570cde6001df365cb216a49bba1b2dff0be3e3a2f69d106d698d30da3277c1deee74d34ebcf04"
                            },
                            {
                                "filesize": 4596765,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "067feff12a97e1b60b7fcf460b2ce2c7888dc9055bb5ca3b4f2d42f2e7ee48c700bc015f6ac1555dc5e94034881d280b9af14ff760d64b48038e059223b64e01"
                            },
                            {
                                "filesize": 5525193,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "9062d9fe4d3f711b77102154e514dd20fa1e27076de1576aff0f4121497c9369d61a7afe3c419fc86c76491b6b1f1a9e79f28334e200a9d8e6f19284dfcea584"
                            }
                        ]
                    },
                    "kk": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 42932888,
                                "from": "*",
                                "hashValue": "d5f58cdf26c208d1bad67ea9ca449b2d209355bde474e6fe6f32706f6c8bb05a2523ee447afe7629f1c5c00b1011d904f717b15b9eb2b22ca57390e3fc8e417a"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 6262025,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "b6dbe37903f4a1ad1a30e209d812d672eac268c51b75757f001182534fb0530a9d53c65c159c252ab7ca6f3234e33cd4cc448bbafb6fa8ce9c687e5125d2e17f"
                            },
                            {
                                "filesize": 4596797,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "7bbbe84b2c074bc7feb77f12fe6c8a3892e1982000c660bba951822ca756d4b324d95ca9c6cdb577756b9dee4c5e400b9946879a51b8afcc1f52c83e769e3872"
                            },
                            {
                                "filesize": 5525217,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "1264fe569bc39a5e1c925c9f1620bd1a027a6640fe4f4695d50745664a9bd193ce4f988d149c1ef8c813989e0b4ec071d52d37a72c41e78c7bc9db3f7534208e"
                            }
                        ]
                    },
                    "km": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 43119478,
                                "from": "*",
                                "hashValue": "4c105d758a4d2800b11340d64d022b305b1a962b3ffbbe441e1187fb25599b5e551d8b6bad7eaa6023e765a6793c0f65d6beaf383cbbffb32085f3a0814624f2"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 6262113,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "d389b39146bb6675e34882aa3a1d0a8559fdc1d7579c796084d1314623056deecf86f346f050a01735c56a2b27637c785f656625cba1059f2a71d8e14856921b"
                            },
                            {
                                "filesize": 4596873,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "66f0fc49e63244cde6ca2532b17e4b414ab239e2a4e64f1bf091db8177016436775cb542e28ab95fdb760636524cd746b481c3bee9792228e82908b7542b69cd"
                            },
                            {
                                "filesize": 5525297,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "d925be1f502b538c9c850f8c74fe50adcea1c1904693d8f1fa7f1dfd91c8a3495957efa8dad089db7366e829c9b6ee5cdb0097325c405a274f982442d2c89741"
                            }
                        ]
                    },
                    "kn": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 42942196,
                                "from": "*",
                                "hashValue": "ef2603bcf4e9aa41a05432c6a55f25ee599041996589cfb2c2d19e02afd61fc0389cd5340bf5d140b46f8acb4e3c4f67866d86101bf6fe5645b6cb5d8a3b03cc"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 6262065,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "b8d6e4a86c2930ac9c6c78cc9bace8361b30b91863733b508ce34eb69aababa71bf3d7ca34c9912c83d70d143807f25073aed726d9dac09a453f689d5110bee7"
                            },
                            {
                                "filesize": 4596837,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "e2a09b6d6133beeebfdf556c77146e87f59e418e9bb61e25fd407de0a491b9ca293f8a5a29dd86d8e10c5c8b07def24069fbbddadd73861b1c7bf5e500f6d082"
                            },
                            {
                                "filesize": 5525253,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "48a3ac8d7de0a39bafc108be8f26b70e6057f63c05382b530f9362b547f89a31012c3b6057a1295b706bff3109c72d6fb80932e818e687b3ff9d4671876fd912"
                            }
                        ]
                    },
                    "ko": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 42918612,
                                "from": "*",
                                "hashValue": "edda128762403c40d863bcdec893fc70e22dddb540666a569c0eed532596d5f234906c5cabff78f839b385be10cdf3ccc94db7bbee37c273159ab7b3a756f4ac"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 6261949,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "5b0826d19fddd37948595de1834c6aa50630219fffcb064af129ba1834b8f967d95fd437341c1853624b1648428263452e9b74f124c92f7e1fc85365c2169f19"
                            },
                            {
                                "filesize": 4596733,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "ac9bbd6a608c3a7b38f66b0a5effdac74d85275db0ad9f1b1f4cf2488dc906b7c821fc1545185468a3f5bd584dbdf79d2e39f46e26ed5c3fe2096954929ed378"
                            },
                            {
                                "filesize": 5525197,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "b283fbd9a7b74165204c555050dc60a0e4132e4e6dec9cd574b73184bfc174cd16a385c565c955dae540b248772ee3c5828602ac9cdc6f4d5518d1cc3d80f2d1"
                            }
                        ]
                    },
                    "lij": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 43099142,
                                "from": "*",
                                "hashValue": "576bb3e5e7a3d935eae04dd2d1fbd2c4c5be0e38f7e1f046fc3d12f91f680591d44eccfcb348e76e2ff248335f5cabf371f8c9bf989954a56dda4c3aabd32247"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 6262021,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "12ea252956d8ba12912002ccb5d32307b2e1161fb255b9b99de69f82cca37aecd3f5c2151f352a62452575d2d0aad46774762a9d50821a7d578873a2b9bcba18"
                            },
                            {
                                "filesize": 4596773,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "3b35c9ac4635e4c820de16c37e199683b94cfd86065b8cf32c7a13752fac17a83b158c506ce25cd04270748b115a9aa8b031e916cce02b47ec2a6fbb6ca45439"
                            },
                            {
                                "filesize": 5525193,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "9a9463cfa2ba52b7e47458502ebe18d5a11331251a28d8e8a8727ca5d9246ffb4bb03f597439418a19f3d1c1046001e25bbd668d906d186673f1b5b17fe23f4d"
                            }
                        ]
                    },
                    "lt": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 43201216,
                                "from": "*",
                                "hashValue": "bd82ffb8927578221edfe02f3a4a027ad2c901a55b9ce369e47cfdcfb940ac752d1e78b6b92e291ab6d1b7423a00c30a671d7b9218f965ecea6d07c04b6274a2"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 6262033,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "9cae7017b1d93177769dd078c7df2db5f4f69bf830c5852661930452e313a0fb8d85bc49a6308b1eadfe636686e000ccac4867375ac30fa7e257919689b216a5"
                            },
                            {
                                "filesize": 4596781,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "d692fab1028c6616edf4f0f2fd7c9b9d89609e3d34b1dbdbeada05d57a570b593eeca4b9883aa3dce10f1466346c3d2b8ea0dbed493a27696d08a6226f764e13"
                            },
                            {
                                "filesize": 5525217,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "f8d588384e47bbf044e34963d6603246a051713167284f0b09cc3130899020e19fbce701f2c8bb2c0e22b89ed65cfbf0cb7a251e53197076bd9995d9f8a1681e"
                            }
                        ]
                    },
                    "lv": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 43198178,
                                "from": "*",
                                "hashValue": "dc17a63e19ae4401974c40faa3c1602378d9d2461458c72b9c0a333a288e58961cd01dd039c50082dcddf3c923e268f55207861dbc03d8c8c5941ed5053c2a04"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 4596793,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "01f57a40903b48fd902d008733898e11cea252186e58fb611d9608bbac181ba20d8e66ad3e542f92d11cfd7a4d122a198338d3c233668a0c3312438f24131437"
                            },
                            {
                                "filesize": 6262021,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "9c1b5e9102235a67f2d11fcc118f848ca8ff0be48ab42fb8e9846f21b961db853e7eba5bb71d180528496efb5215c3a2a8aa89e0481a1677486b7a02bf46e26c"
                            },
                            {
                                "filesize": 5525225,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "2780676e83711a331e171cae7143a33c5af037228e585a2416a7bcd5ce290da4daac3188bd4e14390f0d37680e430744002b3bf71c654bf8934acf8636101d51"
                            }
                        ]
                    },
                    "mai": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 42934424,
                                "from": "*",
                                "hashValue": "55360cfcf9fd79469d1bed32556a7427b9466c73138b035216ac8579358c9946c6bbcace42f26f75078b4ccfb378563ad8b61fd9963bab3c04ec09e4be34e53a"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 4596777,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "54563e79c2302f0badd21e6c2adbe5a7accbe661e09c1829cbcb3647c5338e8a69ac93c7c6dfb496b64a9837a92e1258c927a05a82bfcf48c99f088f6018e009"
                            },
                            {
                                "filesize": 6262017,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "bfe0023654c1102af1e5698ae45959686b205cff1eb40d364af7772d100577fc573884b75cf162302ed850663b71c1703a189cdb5a6828a82a987d25b7a72f8a"
                            },
                            {
                                "filesize": 5525237,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "98844ae09e777db6cac9079b39168649607ab6da0e5f5077c5a3cb57dedc7b7f3e0d6d8a4a85ad3bbcc9bf8129648c7d30badc463a32b106866a10597bd6a8b8"
                            }
                        ]
                    },
                    "mk": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 43357460,
                                "from": "*",
                                "hashValue": "d6f3aa2bf6898c0765af9cf4f831f09b390d0cd56ae404b314d654888a80d72d146d43f7726de58d9ce8a47e2b9fd8c2b481b2ba84efa9f6a2349216489e8091"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 4596777,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "9d0e889a8f27a69ba27445d271b0c92c92bbb3975ccaac4614bed8c5b02d1c6321ad581680419f070e6d9e6204815e848e9ab6a26c99d1b6ac1fa526993c31bf"
                            },
                            {
                                "filesize": 6262013,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "df98c5838a64d79c71553542ff4499320cd97cfe8434a21067ef9cb12764b0c0db8d2b4ff2607acbc090b8912254ce7f0ba2e66353327e79b784204ef9cefd14"
                            },
                            {
                                "filesize": 5525213,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "7cfb57aa742b1bd257b971500e2d28bddcd1863496469398edc33cf24b98a853f6005dd51611d5f09a53323332a46f3b897d6239c6291b7c3e6813d710ca3012"
                            }
                        ]
                    },
                    "ml": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 42941372,
                                "from": "*",
                                "hashValue": "2b5a90d7e27a19d9e5f5096ab3bfa9d3d5ca4a745ba136c95c2218353d502d52a86551dc5737236c27559d2c43f177233a5557015b30b96dc0ec2bc610d757f6"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 4596797,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "6a013fc39bb2fa0998e10fa92b579927acad4869fe6da09d97e6e8228167db473ffd3509826f5e36bc38dd0a9ce018753831eee71041ad49074156369ad52b71"
                            },
                            {
                                "filesize": 6262033,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "d71a54bac796f84021b9ccb5f4a169b95cddf4fc9a4f8c323ed766e73e355fcbe01227cc8ebf98a23d78d75e4b411fd9177fd229688710d0146efee952849515"
                            },
                            {
                                "filesize": 5525245,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "f4bad56d7139973025b22fe64de56305687d41baf703dbbd1c26415d50d6ecd05453f578b4dfcf7d8d79431e14e4ba07a32c59cc5a4727f17c7b2e4777c1538a"
                            }
                        ]
                    },
                    "mr": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 42937768,
                                "from": "*",
                                "hashValue": "c13dacc5deb4126604f2f2de42f34937d2e28b07b34b28fbe188d8c789cd32ba7b4554c542ff109079b8ab7c3e1b74c376af69a1a3a42593857ac8a98734447d"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 4596793,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "2c309be6d11a6b5260761efa72d11a3afbc7f587625ad8cdc89259604efb30dc88d877242ae0dd28cfa0a3ba0dd15e79e22b27fc424e9410139aad0fcc059621"
                            },
                            {
                                "filesize": 6262025,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "658322293a5572fab5d7746e1c753be04561bd3f2666ab45cc4acfde55962049cf874cdc39ee4deab91c09770fb40e64603122f761cb9d6711baeeb53effde09"
                            },
                            {
                                "filesize": 5525245,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "956fd3d03a91252407c3e3796bce91f6a48b7135fbff071decc3d029e0b131c27982a63ae82cea5fe1c3e49d183507b55abb29f7ad26e6ed04b1d67f9de48e34"
                            }
                        ]
                    },
                    "ms": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 42916320,
                                "from": "*",
                                "hashValue": "b8c0f2ca5908d4ba17a6a2414a20d3b04a5cea22d0b881ddbce1bbeaa873afa0fb81f04e2878dd19d6f9b5427ca67911133b4120acc2ceaafc9bf9c469a26726"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 4596741,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "0493ba6cc47d651309f1343ac852909e4a9a0b8b75e291fd29aaf86f207132121d71a73f7ca77978f8c4c071bec438508c84f85d404cd01a5988b9d500aa4c17"
                            },
                            {
                                "filesize": 6261993,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "627dbbdd7bd764bba7cb2b2248fcf902c5a12fa63ca2442916a0605733d89fd1cfd84dfde7966899e20ecbb5cecbc62a3596a1f74221a31019998e267f034423"
                            },
                            {
                                "filesize": 5525201,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "a5c0fcdaaa19c140b6b18db695307113a8f43605b523ff971a5ad910d7c7077928511c6fae8f3cfd5b5801891b626c0a993989fc01a905864ef8192bd48c8934"
                            }
                        ]
                    },
                    "my": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 42939828,
                                "from": "*",
                                "hashValue": "627d4e7c36302afc28c8490f11ea5bced02e6107e295e8e33526bd2cac4570673fef9959e15e2a1a2f7a031e1a65370baef79a7927daaba0913d43cb8b8a63d5"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 4596829,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "f4cba8442aa0d2fc4a7bbd89945ae675cd8c9e491d7e968964941d755de687cdbd9e6f3c7d03b52935b941cffb4bfb2425148595d6fb6ea12cbb9a05177e1ccc"
                            },
                            {
                                "filesize": 6262065,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "b113a9a5b0100b397ac6101473089d22da8da873d725a11fb2ddeb39b5104863359f8893e004c6dbfee1515674924c4072302cf2f6497ffed4ab9ef76b7b21f0"
                            },
                            {
                                "filesize": 5525241,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "8f5c574f336ff69520a8b807e79d8d08a45fe160b70e5971887b539f8cdb6a2b0d05f451aa07ec5f0fcfa0f14bd588aec9fcdc9635d1c67121a670114080b30f"
                            }
                        ]
                    },
                    "nb-NO": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 42914148,
                                "from": "*",
                                "hashValue": "ea698281d9660d40456b23c41ef53f6adf6fd34688c75a766b0816149046b3c8748455ad3d5d17b9065ea1a2afe6f47f675d223a8f55eda2452e9aa4cf8b2d3e"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 4596765,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "61bfc04409b5fad1439e494ca4e43118c4865cbdd8b97e799d4b24751c5ab9078d04e4c7ba3a6ad3049ad2235146aeb22f5b6b136dcb07d79a9b494cd10b07c1"
                            },
                            {
                                "filesize": 6262009,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "1ad791e595e9454a989391935710102b99c671f904daaa2573a044931667c73fa4015371adc50ef71755991511a35b5dc356e2b33f7ff887b6ddabc1aa2bfe96"
                            },
                            {
                                "filesize": 5525197,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "75b62738faf5224485f2a7a1aab9db88627c634930c3d46ac61c15f836dfd7f402631ee98bd21dce42a9eeade71273c7315980a4d63a663c0a45ffb6ff9e17cb"
                            }
                        ]
                    },
                    "nl": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 43590200,
                                "from": "*",
                                "hashValue": "6c3f75c1a61ad0db3766d25c577aa00c027f673f2a5464de648212b0250e8c2cbeff70855c27de1fe9d799bca4470177c7ee5418950b47111598d1d2092ccfca"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 4596773,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "593fa060f8af215057063d9f184e4e47834f23e633ca73dc237481e58bf1e10156e037a2b3f973cb8e298afc957aed0c7d1b8704ea22180ad1f21aa302fe869e"
                            },
                            {
                                "filesize": 6262021,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "298443c1623ed348374e6e04d14fa427acedb806ed853f3974a54ac05d3d7b10f2a0184db35c5cb386d0492dfa6dfd318d092f6b3a00169f220b6d65c7604ae3"
                            },
                            {
                                "filesize": 5525205,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "58cd3cd1977bcc2944452be83347e4ae4ff34c5f6fa9b8c64270fa8f207f6bd33c6e27cfdc4c15c4aa985c97c58cc259f7459b8504dbed9e0b4762981cefaeb7"
                            }
                        ]
                    },
                    "nn-NO": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 42916276,
                                "from": "*",
                                "hashValue": "a1d9f319fc9050e5925026b9b62bf1ac0fafc071c4dcba194b69f5d85d95fa2b16b98cfbf691c0c509bb370cbeade2745e2290e8dac942455cd43006008ce1a6"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5525189,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "04d82d6d65e1d156359654ede2876fdabdbea21ed17c8c78b40c860f58895edab1c0595e1c56b67d1c2819decf03934c795922e3934a778ee9819d5c0d9f0ce5"
                            },
                            {
                                "filesize": 4596749,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "2d25db25f3b5f09439af7e6909700e4cc35340be29234587df35c3e6b1b5c7e5f06f0097261c3245f1d27126209523718aadb32645d39fc7a30508fc17973dab"
                            },
                            {
                                "filesize": 6261997,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "125833642400963c5dab5be804f8b1c080e00b8785a74aa783d2dc570ed3fcba703ac0bd953d7e1b67aae4a6532e7d00b54e2508ac39b4456b5976aac6dcc7c1"
                            }
                        ]
                    },
                    "or": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 43104126,
                                "from": "*",
                                "hashValue": "36f996b333253ac7ef39cfd3c866e47560a002ce927a5a6dc0a482738fae1c66020fca406847871832fb2f7dc26f79e65083f27530b365f092c59fe009777839"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5525261,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "730c617f16091c6170a54ef3f5861c6b8717b887f394c5bb892ddea7b5ef9315266abbb25c4276791339203098b83a401ea5ce4f5fcbfc33855154d3d68ec790"
                            },
                            {
                                "filesize": 4596821,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "c1d8beb8394fc0403869634488177e7c7857368968339e8bf7aba308cd33b5e01caba884bb4a48338fe405ca4a6812161f8381795e78068f7d789b2dec4ea6f2"
                            },
                            {
                                "filesize": 6262069,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "3b94fccf08f9378bd00c72f707f0ff171f1e3f2a5e50ddf798a3b90dc149e4e18da92431c44d2dba111fe22056e69b44cea68e1e0d1fb03343bcb67bd19bed4b"
                            }
                        ]
                    },
                    "pa-IN": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 42925828,
                                "from": "*",
                                "hashValue": "bb25f97ce5a51ee7b3217e597ab3603a9cc9615c95a19d23dc35ce98b28c8a503b062ba3bbd15e22882d1286cd54bc28a2d05c45a1ce9085d79d23e0a8280fe2"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5525221,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "051d7b55c9a7937d7474021e4fdf5cc787544641fc135c6a00f9ef505fa7f1799aaaeceb2f2da202bf2c1725ec98d2b1c718468dd3b66d0a490011356a1c13f5"
                            },
                            {
                                "filesize": 4596793,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "679c2e1fd4c784e1b38a5297a17703602f0694e114f7180cdf2b861355c0f8baed999824e4e30299c2b0cca5f458780037f371ce26d22248aeb89022ee505c12"
                            },
                            {
                                "filesize": 6262017,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "31f63d04582f536df2be56407b3331b11cd9329b6a69284d0153ee75da8ec8b5c0e4aaeaa397d229aecac208359a62be31d0ba65e98dbd6ca3792e2adbf8f5f2"
                            }
                        ]
                    },
                    "pl": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 43838996,
                                "from": "*",
                                "hashValue": "fa47dcfd1f6d148107d23dd177a815bb88c82cb43a8bbcc937e92ee8d4af4bfae972dd2aa31a8cb31f0e21e9b443f03dbacf01ae1a10ee863e5c933a88df69b0"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5525153,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "d8b7802eb214ef910097047606715e1e00e89b82a2cf5a0c26dbbec86c71d8b824b4010660a203500676832a5134590597b3246bab6670e927b2227d23b1d767"
                            },
                            {
                                "filesize": 4596709,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "24c46cdf1cfe650ffcff6a141a7597bd9e00f9d1947e3c1ff9c9ca23e462c9af0ad0aef00befda0157bd0f9971c45f46dbf210e8a1c0270677fd27a92baacf85"
                            },
                            {
                                "filesize": 6261925,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "4691ca0b8dceb765f3df0b0bc8b9d95f485d5bb77cf938fb1d0d2a35bc54e2f7566e1397448f5d3a196083666f2b4145c323c3705697e1b5459c91dc6e44a2b1"
                            }
                        ]
                    },
                    "pt-BR": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 43068602,
                                "from": "*",
                                "hashValue": "8262192c7dd42067bf9d360904ea6db0f2fdda56fa1c1db75636d1c0f779d208e4d9ce86f0fc07f0c7455c84e0cb8d2a8ef25debe013f1fe9144103397396fa0"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5525229,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "a72c41a196c0a220e51c2aa23e139c1913c624bd68ee1d8570e07febdabe7318ff67c2667fdcb44d7a9b13b71712e79476341e2c023db5898bfd0afba0e8c28d"
                            },
                            {
                                "filesize": 4596813,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "8d55f97f6506ce21e2ee35c9d6b0133518c27e8f382362ecdd5c47c2a4848ef28205c2d821e5ec07c92d61f8bc5b40a0126f229d93638ec67609075b422c9c0b"
                            },
                            {
                                "filesize": 6262073,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "aa594dc8de3795454bcdfe2c15888323e46bbc79f1a3a0a156eeedfddb714be00e297aa3d3358bec6c7a07d744459e457910cc313ea2a5ceeccd14420abe9845"
                            }
                        ]
                    },
                    "pt-PT": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 43096262,
                                "from": "*",
                                "hashValue": "91ef3b2e0682a480817dd9d46efc50d708ad0ce49476668138512ee755fcc9726afbda6526a24f4d33b1d1f62ca25bcfef0615ee5295300d70b98e7b71991554"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5525221,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "9444bdcf358feb9df80e24fd5df66f27441f429a762c2873bc8c5c416109ac111e16a1deca652a2f244feef22a59c97086c60f82cf0f1a73f85cc29ad0021b97"
                            },
                            {
                                "filesize": 4596765,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "43a0092e604e67ff0d57e9f0691ba7a48e6253fe58c7b273b32569a3223244416c6c50efed076ca822e06659acd1c85654b537d209fabb1a963e8e6f31acf629"
                            },
                            {
                                "filesize": 6261985,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "7fb531cd3f2fb196e6116f115503bac8a66785d585a2c5e9732cd4946064ff3d8b1cd8c828b493ae9a8b990b3736f7ba935a74c96ea2d760f1b57b00efd28402"
                            }
                        ]
                    },
                    "rm": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 43103164,
                                "from": "*",
                                "hashValue": "dd18565b7461f21c29d7158ea3c340e49ca4d712b2559f12f838727ebe7d2966161ce9b98543faf79992eec89e19e5882a8cadf2fefe78bae4daaaba9dba6f36"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5525213,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "3fa296abc02bae0c0208833ffa8eeb81efdd8aa4ca6b37df528b2b109e57898e11fd67a53bb72623a15015fdc1252f0621fea27d23174e178c3e97751d8624eb"
                            },
                            {
                                "filesize": 4596797,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "cb5a8457607354b38891c3e6d3857b3c4843d94f1fb94c48a0f81943dce694750a09744f0b6559b29f5ddef300a7013639cb097b5cceaab912bc5720a2954d76"
                            },
                            {
                                "filesize": 6262033,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "be3ffc1012e641e908a49f1be40d1b0b647ac3fbd31c4f9e5d1610dd4009aacf9b5907ebc25559d7ac08692d8d9b339c557a581e7039bacba415ad3b6741b089"
                            }
                        ]
                    },
                    "ro": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 43406160,
                                "from": "*",
                                "hashValue": "6e94b705169a9ec4bba2cc2ba514723d4459c4dc70325cb66ab99e52a6e7f9213f79b5c107f747a7dd8aa0eff8ff93010309d3398e260c2719beb97102ed6d90"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5525197,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "9434479a0105338a9433f72fa9377165e6d368805df0d38f31660e3fa3031933d6818c8093a1b3eb3cc9a3eb2d2efe2f1656fba6ecd2ce8cd6e8db37d4714189"
                            },
                            {
                                "filesize": 4596749,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "bea30cb334214e65eca9ab8e5b72ffbe1cb682d57aca205dfa7ec1ac95c481f2aae97df2f2ee7e5465412825f76a99e892241430331dad8e4d23c89fe38da498"
                            },
                            {
                                "filesize": 6261989,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "2e542df1b1d72e4188b4b5d8f29970fdf276f4c9fe4ab3ab2731c8b528e1df3ff3630dbfc62e28d1c2a29bd4db06175e1ab0c312a150a25d768cb0a7575d0264"
                            }
                        ]
                    },
                    "ru": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 43361084,
                                "from": "*",
                                "hashValue": "7dccaa77533bff6f7dad15d10bda0cfa034cab6dbb7fe06a715f9e83c95ef3e7ee944fc4a88aa676cf1e10f09b219d6e7d837b6031c6e6b62d91050292fa40b1"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5530185,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "a5bc26701817b98c667cca79f62ea8a09d95d802fa6f7f9ad58a4df1ee9a0b6f5bf70165734d01914754c9adf77a8f2e151edeb9fe6b2d7449b5addf1641ce7c"
                            },
                            {
                                "filesize": 4597889,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "5cd026a60350dd225f2594357b01fcb5df1b085663a4c9dec52208336a9b65509ab0f16ec2aa008a4f3c6c8f1dbcca8dfa5869c2eda20710d87be3f69160b70d"
                            },
                            {
                                "filesize": 6263113,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "92d000cb3ea75d92d908cc23a763acf436fc75bef826fdf1c6e6a93e0c24fb0cb4a3ed104573aef66f38dca8cc4efa3823c46b17b128befb47ebce91bfb50961"
                            }
                        ]
                    },
                    "si": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 42927792,
                                "from": "*",
                                "hashValue": "7b3353198bdbc0c446613b9a49daa6b228c2899c612a5b45ec36e88697e49ae7c96721991980f9023552639e4873ee4f2ab6cb9da4ecbf5c35bb4041aa9b8660"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 4596789,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "48053a923d52f8b24468caa2ccab5feb5defeb668f67706e2b312e3193d622ca698878c748b097d97a755197981c42ff962a25955015034a6ca09c66808fb81e"
                            },
                            {
                                "filesize": 6262029,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "0e939e8abdd90cbde6c0e69008d530c21ba7bf3e7340103847ebea043839465db534c575d661459cefa054752ac774846d7725fe4b6d77eccf0b8e6ca8fde2f9"
                            },
                            {
                                "filesize": 5525221,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "7ab618145264371a374f69658a95905c8f7f22e692ccc8bb08cace00da07107ec699df7c971b173bd360b8452d893c152276b8bcf85b71a9a132920d563c31a4"
                            }
                        ]
                    },
                    "sk": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 43612356,
                                "from": "*",
                                "hashValue": "6f3df2fd16da372d73f0191c86725759cdf7a6e19ab45c35dcf999a53c63d4e1f4febf907b5ff60ce027d2f5221612638c29c7e0337c340259495c05be427ddb"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 4596773,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "a0007023cb5b943073d4b8ddd4df99f6738e6d5d97cdc9f80c3ae16bede14c48c143b21e27c9ca287aa06a7a7870d476a1b833640f9c4fa6850df881d832110f"
                            },
                            {
                                "filesize": 6262001,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "15a54bd939dba13c0445ed6a99f99a9a547fddee659e6540caf152a5c5c4fa7571b2badb6bdb333d23a22a14ba09555b321106c6cc1d6d89daffccb7c5bf970a"
                            },
                            {
                                "filesize": 5525217,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "16d1163a6ecd4e0d2d638c416a9e7558aebf9d8c0ae10dd9dded9582c1824ea5816cc04759e241d9fe960a4cb234fe667f296ffb2ce006365413abadfa3f852b"
                            }
                        ]
                    },
                    "sl": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 42923724,
                                "from": "*",
                                "hashValue": "fc18ff209ba2af2e806575723c162d316210de9c8e062f232c75e04982198c293593c747198dd16411c71cac526aaa7f2529eb048b330ea3a46530efcd86d6f1"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 4596741,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "f6702740a1bfd9cbdce38444f30cc9fa8e7acb0588c4e4927921b0d5399ae56e5a31d337c263688f7a022ae98b1c134e2733b67b6304b94ee5dafbb39a52ee24"
                            },
                            {
                                "filesize": 6261969,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "68a4ed652b0cafaa6fa0818d4dd0def2f3fdf02bc0e185cd0153f4767c0cf39342d607513574d183b090ee649c5cc0612d8476e08a4e5aa855ea2879b1da36d3"
                            },
                            {
                                "filesize": 5525185,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "687813d20a5b1f866862602488140b2e11ed70f4003db4acb8c3f4a5966e85bf33c74d8716047206196b0a6bf369b228454c537580e395cd1c175f81a9644d3c"
                            }
                        ]
                    },
                    "son": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 42915532,
                                "from": "*",
                                "hashValue": "a1aa2a514a0c5e8c2c5bbcb46068ce944dc0c0e80da1b751354ee1c8f4098c0c784d6f6fadd802391421a94a3bd360ed18d8e00f6b012b9ff53911fcf49bd92c"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 4596749,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "4929e4882a2e2a54be036723316996aa16005956a96d26954c22b93b21714bbcb974c67d5bbd97483bbe55e83541a6101c8561dc433dddedb1763fc9b423afeb"
                            },
                            {
                                "filesize": 6262005,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "5c9a2511c20f48ce203042cd51fd3382c824661eaec8bfac284ed555a76064ef3eed2d1a889056b175371e9ced7f11d77b9b949f66ef6dc02c64e3cfe48f3e5e"
                            },
                            {
                                "filesize": 5525197,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "dca1be1b4a6b8f295eaa31889076c1b9521ebd64f61ace86c6a130d334b4e699890e307b0c15402e20f8a8a6c2456a11fa91ce2d988fe88cdfdab529be5676bd"
                            }
                        ]
                    },
                    "sq": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 42928132,
                                "from": "*",
                                "hashValue": "9c720579a5c9a72c199344fa828d68db937dc2d59646ca815d66c5da12ffba4fab3253c7320f61868785ae07b3047538b7fcbbc27b5abbec6c9cc75fc37f12e0"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 4596757,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "f464a1a3c2bcd32e8ce587079bf7f8051394d33b3f4706a6ec1db12b276ff438364c6bf78fee9a251a2d01d53955ae90a1213ea6b5fa7b97b19960a05f49038a"
                            },
                            {
                                "filesize": 6262005,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "c6c921dfea23956646e14bfe4b343226e19e953f28d75a012c4c31d3d2c7ea5192859c551e6f74760faccba51fbdcc746c184fdb714006e8ed8d96f4c2bb9b1c"
                            },
                            {
                                "filesize": 5525185,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "5ff1fcc3e52875dd31e1b5eb921c8691deb90317aaf3977284dc761076371ec23798b6577936daf7f44fa92852391875a6a6bf579c8e29f9f87242eaf53060c6"
                            }
                        ]
                    },
                    "sr": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 44049972,
                                "from": "*",
                                "hashValue": "f050df9deb5e05cac7a67c6ef5c3539940339429dfb32b4e5844ef5bfd4b2d5199a698f2aaa3831ba8d2e838880ef9055627e1c079a158437bb0c16fc6069889"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 4596785,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "9d1a77efa3bb76288e93cc99b3186705b9f5640f5491835a38b2a62339d89deac002e2f40f7efab91b553d82a5463f623ce055e69cd7a7440786dfa475bb4a47"
                            },
                            {
                                "filesize": 6262029,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "5798a0eab7103ed17b3644e0e8990e9cd4de815aac0db26eb022333d572391c37f2fd6afb6894659550778b9b786b63f008a89a36d2db5b6a7542c655bd7901b"
                            },
                            {
                                "filesize": 5525229,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "864164235f1b504b987c7c76c4c98142df3f04ff2845155bcacfbfeca94655dfb135079f57954e1c364338c0c5de2b5bde79dd1eba21a1bb5eb4bdaa46f578ac"
                            }
                        ]
                    },
                    "sv-SE": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 43460512,
                                "from": "*",
                                "hashValue": "7c4554baca441b93308c076bb4002d1fd609cedd1a1a7f738ac51b8fc1d15dd37952f20a68032062518424e9e0b6fd725610169429adc608144a46627e1f8291"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 4596793,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "320e12a44df2683c27a6bf4bb8e7d83ab210b5277b4d6736b3a07df014393aa8af0f282bb03e29af995ffc476541acfe52644d3694a0d9409c8e5ecb421d11dd"
                            },
                            {
                                "filesize": 6262033,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "3c6dc4a30734bf8049868fee9a6d6af908c98259957154bd5a1b3cbc40ff181e628ba33ee25bee65ef8bdd4d7fd43890fef679064d679f5d3b07309880b09768"
                            },
                            {
                                "filesize": 5525221,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "43620ac132718d5a84970a50c2f85fafb8707a0dfb70108e8953eb5f7bff8c814c437ec8187173ea87d60264e68492b9bbb1328a36aaf8cf22f8c2f7a4243532"
                            }
                        ]
                    },
                    "ta": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 43138430,
                                "from": "*",
                                "hashValue": "5a1a66963ad89624bb283660aadd053558aacaf9d28b25514f3b0061cdd6480056a24bcdccb2af1f6fc732da81be58b75b9fa5e5c8d5f7b93b295ead7e5281c8"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 4596813,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "5e21ddbeca89437213353dc0e98b1ac11a2bb5b0c2f608c6d1b116854bf0347067baada7ed1ef177d68ef1306cde6c85ddd27fb6466e0ee5f0f903d22e3d654b"
                            },
                            {
                                "filesize": 6262013,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "910a541e021e9756a1a924761f56cdb3deba6fd067f88e623ec7f9e9d27ae019f1637c3ed633bac39f251487bca5c4864f2d957d402e511c2afd999f836b054b"
                            },
                            {
                                "filesize": 5525261,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "a3bfea084618b918063279705106c9e60538c3c45dea4c440a8e565fd0a4d1a8afa3effb42305d9503b76e52b7be42febd41555c0dba07ec13d55a4432d92261"
                            }
                        ]
                    },
                    "te": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 42942604,
                                "from": "*",
                                "hashValue": "da9f3ccc517570e65ab6c9934787855d1ffda410c6e51c0cf5e7a095a7cb7ee2c837bf99ad758e953f83df05091a02a78f44ae54153c3ad3ecba6da95a8a9645"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 4596817,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "7c89e40ad787552ed5498e697ed2e270f9a1d65e9838e877e24206a5f2b5481a7f85fe4a91a6c94e203d4f7e71baa1f71fb425dfeead6a0329d3eb429f5df2fd"
                            },
                            {
                                "filesize": 6262049,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "297cebc90a584cad156ef1966db52ce0f69079b488095344d6a6f6a7bee64d028280d97b5a22a9911e36f72985c171454f0dfc4bc236cafaaf353f8f923e63e9"
                            },
                            {
                                "filesize": 5525237,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "3836556604bf6de4022f790e6df6a5c236ea9a3039fe01addde360e594efc8a697279755bb90fdd6dff337c1d1a48e9b2f6d7d7f9e6bb4ba47b89cd80bf54cd1"
                            }
                        ]
                    },
                    "th": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 42922692,
                                "from": "*",
                                "hashValue": "011542da3ae0d146d8fcacd2522372d242bcea8e96a4368fec05de16d775fbaddbccd762d7ceaf4cf6c744a63a221f80e3f771f27a9fa0d5cbf9d952d314cedb"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 6262033,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "6d18f932c36ab6c98fdaed2861dfaf7755e427e41538fb2bd26d9cbfa08ee41ca63e52adb212410fc9d764246a98ad05805d1e8937d4eff64a034274406fef27"
                            },
                            {
                                "filesize": 5525229,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "49722c881855f613db556341f27ea72e63b4a8921ee9fce4b162e8ae11cffb94d41da189c5aa74816ca0573938d1c798521db95e808d8f6bd28dd3c6d48e0477"
                            },
                            {
                                "filesize": 4596813,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "72542fcc522363d245f2ba86819bd61aa83c5dc5db0868664b1958d0a8c0e91cc03c6d9e4cf055fd85b8dc88fc09cafe7523994bae25595b4803b8f95b82cece"
                            }
                        ]
                    },
                    "tr": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 42921892,
                                "from": "*",
                                "hashValue": "9b610b5bae3a97de5bc5180cd1356b221635aa09bd0736a589a801aee9c5aae3e78a5ea672ca2f90f37cc63fe6be9c349829fc222b3a137c11bd51e47360da5e"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 6261981,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "4f2818d1d086b9e790faaad3ab9466be6087e4269e5f6e235e714224c5555eb7698bfc49980a6afddfd0cf9b066b8cb9e76f9eea3fe20d0a33b3925a7646e765"
                            },
                            {
                                "filesize": 5525189,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "bac232711b6289b45976a885655d118e40005c247752fff86cd40f841d7ed540a8f1c5ea33fd02a1fe48a1837206f1a822f561916853a708424fac14629d4588"
                            },
                            {
                                "filesize": 4596749,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "75341898baea15aae3a10245082762dfe4c02182ace6a57cbb310e18eaeaf45ab6d534535fc99670cfb7feeb4917527fcb8e6253f7c34f5a66a12031e7f5c09f"
                            }
                        ]
                    },
                    "uk": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 43811028,
                                "from": "*",
                                "hashValue": "31a2ea25454d9e6c444c03fe928d1d8cec2691ed267f0dd69c08ea8c1431b3fdd83ef161ccf472ad549bdb3ca226f4ce3356c9e375d349245ff5110c5951cb8b"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 6262013,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "cf0cbaf71dde118250430c11289646dee5a6ed0d2a9a78a7675977872c43baceb3b20891b0f283b399ae4417c99322ca317a6576521eeb8ed8922d9d4e6388e6"
                            },
                            {
                                "filesize": 5525229,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "708f9bec69694090775bfedce684823a300b60c671ffcc8b4f7b96e3b7a8644667b14222274f00c46e2a33aafd131d9a3c5ebf8d3fe7bcd3e61cc376a91efbaf"
                            },
                            {
                                "filesize": 4596805,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "7135e7cad496c5cc2ccfbd59ea36d8ef5a8a702b54a01c1766ae5dcf31c96b02271cad562958c7af0f557114a7d33c0435aa4e10d3d8e7df081c1ec7913924de"
                            }
                        ]
                    },
                    "ur": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 42935292,
                                "from": "*",
                                "hashValue": "ed320b90677c8ce561193cbc50a62d14f84cddd26931d8ed2d5ee1df89953e39b2be2de45aa313b2e1dbb46af0bbba773834f29ee9c99126f7f0d691b0b1ef9e"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 6262041,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "2e017007a11e6b5489d7060bfe4e9a323d5e4c64ab029c9dff0bea30cef0a283eb095492e964d7a06b2f9aa085a2bf9a49b7c81f7c7eb2786fbaeb3eee7549c0"
                            },
                            {
                                "filesize": 5525213,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "5602fd9f2ae4252f40854e64c3325d6728aac3b69665e5551a95b32e83366617043a78f990461f41f1a3e8ee1dfe796af3ff1e19ea9b7d27f0517df697239a8a"
                            },
                            {
                                "filesize": 4596789,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "3cb64a411276974a8cdaea59129af4de702aeab029795598019a375481a0ef5ddee90f48f72385a27031ac184a8ac850fb8d7baa5881c16344f94033fc9b8ed5"
                            }
                        ]
                    },
                    "uz": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 42922180,
                                "from": "*",
                                "hashValue": "5981719e35de424d6e12eeb995e97f2a1e3f1bf02b0434d079b653c70b911d07d2f223e97c317efb2fd377ff6e41360125dd6b1f84dbebef556b386f4a9e6d23"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 6261997,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "21d50585d3b99071c51a94ccc82537258a2ba9b6f6c08e6b65abcadbb89ff31ebdd6bc756106fdc141591366919b05d91e5a19e2403aee524966413a42e2bd20"
                            },
                            {
                                "filesize": 5525177,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "f523b5eed9825802b39e6c2d651d4bdbc030a733fa061949bc2bf6bb08c426351e489e886a0192592f6115d294f2e8ff6631914c07c54839ddeabc67c1bca286"
                            },
                            {
                                "filesize": 4596749,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "604f076ddb61cd7f3dd8097f2697d39226cc38cca4a92a85552cd9d1a6b59a0fbf7f73e1cea005592058fef11d01f0b8caa6ff466b6923585a83950692e14e0c"
                            }
                        ]
                    },
                    "vi": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 42936416,
                                "from": "*",
                                "hashValue": "548e2ba95b0b041240b5aac445a50984e5fcee016babb480b5d7fdc399cf4e99a048caf712032fdebf3b7806180978c55a150da8059f84dd42a178aa86c061e6"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 6262037,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "db00da079aa74ca75237ec2ef289d002b782afb11b075ae849f82e205c87815920c91ce64bd522d0c69e7e57b3822f651d701b7a0d7f0337667276fa157a2d48"
                            },
                            {
                                "filesize": 5525261,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "2e742ff90f777d708c7efdeb3824da444eeb3295f4644cd7b7e7cbc282dc330eb74280a2bfddd6780f133866fe72ace26aab2f73e310b5663792d57af1a10dbe"
                            },
                            {
                                "filesize": 4596801,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "1648cd7d010e662cc46938fafebf96d6034a247148ec629d651b44c90ab5cf832b8e72a8956ca10a57ed79d807ee6b3d38cf43765441535f4f642fbbe95bb1da"
                            }
                        ]
                    },
                    "xh": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 42928456,
                                "from": "*",
                                "hashValue": "e1889c0635ea3b5ee81975ef296a61182f2dcc6bf43c668632ebac2f863589a37753064d22685e0ce830e1ac3abc2a6cdcf517015759f5d224da39255e4d13ec"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 6261993,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "f61095132005804cb4de5a7bd56bb0f0b0c9e4bbd825af790968e3c1b56ce665e6b2b3418c1a64c5db9b273a04dac1997021f015d44aa6d7d4830df288dcdb41"
                            },
                            {
                                "filesize": 5525181,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "b6b33af5fed7655a63a63b3966bacca24bb960b08f6c7c240f767398b28ff8767d80cf5e9f09ceedfa1f2158fa1a7588cb19225473f4a0fb3be857e6571dd4a7"
                            },
                            {
                                "filesize": 4596741,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "8df87b5adec8155e688b9e875d5ebb73b293d544eed44a685b501b101c40c6e0562e4503db7be28ba9b4dce14283cd74655097725b4288be6b366d4470826287"
                            }
                        ]
                    },
                    "zh-CN": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 42917920,
                                "from": "*",
                                "hashValue": "80fba4ed8afd72726ae7ad6c6fd55dc307e8b71ad6537749cbab2094cc53306127959691297b14c82c99c4cbbcec5a2bbf3ecc635c9c2c36bcf8097e3ca9058d"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 6262005,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "dcea5ca988bcc92ac2c046f0a3d5c6f457eb1efe89633726eb64d3d9a835a5ee022f60718f327892ee4a586bd5e43ec0d5fbf5b0a4c28a622591eb5252b4bb72"
                            },
                            {
                                "filesize": 5525213,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "12e19e8ae9b30aa820c9a6202e17a4562e4ffe28d842f36a00ef5031e9778c9db05ed388f664a4117280f3b3826230b3c633f9d1878c7faa92614663da24c04f"
                            },
                            {
                                "filesize": 4596757,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "1b2d72d1527ae4b0df73acea1f7176d22fecd05fe2bcdd4a4b39c1822a2c6270f1d69c7fd796c0fbf3b62635ea479177f7a622b05599e6adb7617e5e84bab4b9"
                            }
                        ]
                    },
                    "zh-TW": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 43093498,
                                "from": "*",
                                "hashValue": "9c958a34741ab2d57febd37f4c23c026d312eb8bfa58b2116fd99e332be0e69eccf7aa06ddd6f01a3ea2f624ae549c5e9899522fe4e8a012e8f79b58292df545"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 6262209,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "f39848c282bfd883abd6acf4c8a826589adafa72f13188dfb59f7e25b712c31cfc17b28dc103fd1e82b2da5be10dbd968bb8df2dee97f61cc2db8cdf07e8c52d"
                            },
                            {
                                "filesize": 5529417,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "b3df53cf21a61da1d9a333274d8bb75aa16da7e3a54152f91f8bb6431a9ecbed6425ffd49ee03efe0adf24ed1e39e95916ee6d6b6a70b98c81fda95601aceff3"
                            },
                            {
                                "filesize": 4596993,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "80a2fc99dc17789d7c1045c5763218d568d115922a39cee08c5173552c9ab6efa8f894323c1e617727b4982af57546511158999c5a81641889d1bbf74ff38da9"
                            }
                        ]
                    }
                }
            },
            "WINNT_x86-msvc": {
                "OS_BOUNCER": "win",
                "OS_FTP": "win32",
                "locales": {
                    "ach": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 38024136,
                                "from": "*",
                                "hashValue": "a0b0458aa78b90d2e711bbfff463ec399a73318e361c35d4deefda14ceab987b0e5a4b0e0f374cd5eb9d8ed1cdc9d6b6fe07c90d6176fc8efba4bfc41cb3fa87"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5247943,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "143a73953913faa6167e52ba668828d86bf6034f6298defdc36124e9ed7271a1cb140adbd764eb966bfd839858190b22394db15106707ca0f5659c7eb9a6f787"
                            },
                            {
                                "filesize": 5295019,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "e773a3f99b5db8894005fef162c261e9767021d09ffc72616c009d5d4f40f461a603e86761484d7a72b792873a8709eefe323573384834602ce76598e2135669"
                            },
                            {
                                "filesize": 4815515,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "608a3f0c0f1e47c7e0f9c7d393c4c51f8ed6ba2fb20f96b75ca5dd71ddda1f0d00851d0ecaae994499f1594404e667aaebd9fc99454f73722bb9a2cba3933e6f"
                            }
                        ]
                    },
                    "af": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 38023816,
                                "from": "*",
                                "hashValue": "cedc1e8cdf79a14342f1accc80928c7c25c0f48a4c79ce268b985137bbbe9af04291787e0cf7c6380e6ad07a0e559ca0594d54ac1cb73722598d61db4152605a"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5247955,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "b84fa0731d4202297cf0b14483c174cc9f2193da3300bbb92a19e7f1c03dc88034cad2aefb1c6c7c290f5db89454083606fb329857dada18929d3dfa06035758"
                            },
                            {
                                "filesize": 5295027,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "6e803c5c72373791e96c3335a4f8b2482dbb5cf097988c810598ced8c04854bb9310d3f5c63666ce2e1349655c288143086674735fb65483ad290655a9b6f1ca"
                            },
                            {
                                "filesize": 4815519,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "ad5e5a4c673161c2bfc6eab54488d94f4edf41e885ad68565654a3eda2ea5f4eaac1aec3eb36ec9300776d151590b6f772a00aa33ddff22b3064d364becb4f27"
                            }
                        ]
                    },
                    "an": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 38036388,
                                "from": "*",
                                "hashValue": "164801f237bb1adf6665015cd7266830c072c29594b1afa91c64d3b7d444c62b947bba1fed43209e00aee7a18cbc6e45691c42e46dbb2e7787aa13f9c22bf546"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5247955,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "679205d73edcb6531f6b4b67022d4f3cdda3e6da0a3dd5cbb7d56ee87b123dfc2e5396d79fef3fcc169f1208202aaa2150a4229c19b1352b058125e53f329b5f"
                            },
                            {
                                "filesize": 5295027,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "98feea8d6cf45c36a87e06df0a4c4e9f7fa74db3734452613867c836d5186fa7126cbe77bb1d751b1ffeef764ea34d9b48ac443cfd4f489148d121b6aa096c2e"
                            },
                            {
                                "filesize": 4815527,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "827150db9598eae93452a7e9fab0d274b5c3176fd85a63143b136b36135d802c66b1bac792adce12f651ba7a7fc0042973f4c7c0d53868e3a62a55f9a8d1531d"
                            }
                        ]
                    },
                    "ar": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 38040776,
                                "from": "*",
                                "hashValue": "f202150800a047b2db5e862c0846f1fe157d0cf975ed052701ff227b1322e26ed03fc8f37748db75566d1a3f1eef7a83ee94c74d04b134dcdfa3ba07eaca7c1a"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5247967,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "b5bfc5fd268c1e3e651124c303d2601cd6b797c862076e6d2e4d5aa1be5197365e384ce8e102c6b89e06d5a29827d70a2160a6b6f28aa5201752e51248c362f4"
                            },
                            {
                                "filesize": 5295043,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "8100c625aec9e1fee2bb284583c6931dc7fdaa81695e8c1d236dab20d2dcccfd9de246f6077343df2bf1ee88cd8a3404369f07bce8c1a861d4adabac39d3c237"
                            },
                            {
                                "filesize": 4815535,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "01256ee76ec68c5f46f2952cd10304b437aeb6963cf778ff1389b7076d09be0d7119bb0f42a1ba4134768acfd55a3f494e721c8a6f006cff0b51187492c0f801"
                            }
                        ]
                    },
                    "as": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 38036268,
                                "from": "*",
                                "hashValue": "042e839120158ecd9f4a65eec85e2bcf42d18f656f5815511cee82ed8799b785b88cb4447fa01831f008898dda94ed211485767fc7cf53f9f6205049adb152c4"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5247975,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "ed95fd327608d6af668050363085b1545db7cd5ae54c66c7a82f851835143e8cd87e0460d0e10eef1f9a7757de05bfc38696e340ab5b4d31a7fad8f39038b289"
                            },
                            {
                                "filesize": 5295059,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "166cbf4ce3e783992a4d826b6c5c0dbf6dfd37464d1f1930adef0ff31bbcc9dc3931e42d5ee3e605bb1f464f61ec680532de28ef373eb5a6e1ec4b63faf5eccf"
                            },
                            {
                                "filesize": 4815551,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "b96019f960193d5f1057b101f4b60eed2b75895815cd1bdec75ba0fe2d253ac3b6e067127d474ecf2f49b4bd840c3989c935f47db22724a66bcb6b9b9470bc30"
                            }
                        ]
                    },
                    "ast": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 38031876,
                                "from": "*",
                                "hashValue": "a62cc1c377631bbb9bd396802e04d8fa5226acf57f39d0be0a6de6487dd2927876f6f50d598ef938af27e511f833b48dea6ecc7e7c33dc3535130aabb6db6ce4"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5247947,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "dffefb3e8752b929cee590e1b2c181e9d4b713df7af066deaf911258b232db31c303b77a5d440e99203fc3e533c1d961b30b145813ae1629a9c1fd7da7019d40"
                            },
                            {
                                "filesize": 5295023,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "d15625d59c1dcc25a5a8de103c9b62e2182cd43f65e0b101f12bc8bc890240e3777f1767cbce403ed8665b72791fe43f3157a95b127ad7434cf4520b015db80d"
                            },
                            {
                                "filesize": 4815519,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "27dbc3736e6bc319079eff9af84a4eaeee8af37794fe8e8e1ba65cd49a54ea1164a0c9e72f2ceb5a7cf6e5374cc8b2d09bfbe98ced7b3803ec9fd249d929abc5"
                            }
                        ]
                    },
                    "az": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 38033104,
                                "from": "*",
                                "hashValue": "9a83791f34da9dbf3afef7aa4e4ce361c4d19d6f0f58a173a48630fd56ab04c1648cf0965befaf3e07dc68e9a0a065b8ac5e4b74e2ffc5cf3e122f4aa6e85aa3"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5247963,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "5119d9790ea2f6f2d7b80a15c32b2fd790e6ba3ac101c5777e2b0b39c1b88834744e76c114a2bf9854ffd27249afbfc45d20e5f80928f235ef70cba817f2d678"
                            },
                            {
                                "filesize": 5295031,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "66c015d89a96a6a33c2aa2d68c3d32d814049d805bc525682542fc7845fd924ede4717bfd6e87f79991bd266bad0790f43beca38658e9ce2cb9f140bf5674686"
                            },
                            {
                                "filesize": 4815535,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "96344127901966ec70e6ba29600116e2e359c5df1d400381b12a3e8243536062b89af2fe3fd01a70e38628dd627702cff50390646149a5f6435d8f05af597cec"
                            }
                        ]
                    },
                    "be": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 38046532,
                                "from": "*",
                                "hashValue": "1f0f723802805697499eaa4495006cf032a6a163f0342c84fb06bea449f178544a43fc6b41303fa9f068d7a5502b30465fda35199abc7868040d67342c1b1c89"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5248003,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "de972be2a6c944a13f715b5eb4e057d4a6b52115c4b4e7c2ea8bb9118d406107010c21d3fb4be1603d0b58f359c059526fb96333485ec859eccebe4b93e50755"
                            },
                            {
                                "filesize": 5295059,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "6133cb2b7e60c77da701d3c8ecc850272dfacf3df02d8d13876a52690b8c12db08c309b1f5c6f95c69ceb438bcd9a69b45a59b81dcd6235e8f9582676ae384e7"
                            },
                            {
                                "filesize": 4815579,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "1ed8862db038b7e8a4d566eb317cc01ac8f400d432b5c58576429dc72cd27680d69da1ff618fa7a068c398fa312a7336db701c72c451fffbe5da37aea135e6b5"
                            }
                        ]
                    },
                    "bg": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 38721948,
                                "from": "*",
                                "hashValue": "3a0951a5d80a564cabb1e75623be8d15404d1ed76749809a7d2b37a0f67e244e88e5a874154e8b868cee760a41872b53e26d58eadb60ec6ad809025d0af7b2d8"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5248003,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "3e27ef101ed3f4f0ac90e9962ce23522970758299ef2611f226e87ed068ede49d3205b810780eff05d9734ea609b400b2ab2c1db722e8c4c220ac5b22dc0887e"
                            },
                            {
                                "filesize": 5295079,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "a9ac2374ebee6d96e047b7bbf7c172c035675f0d5bb59c8742c6abb529c385fd42595b7ec09f1faecd2c6e315cebfda0af8042975273287b414abfce241fa65c"
                            },
                            {
                                "filesize": 4815571,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "10c100a02b33b11b8331b736ca43e9394a49745d822888c481f153cf7657040fe4af4e0e451dbf4b94864b407ac5f62c741c1eec708568ffca4efcaab854490e"
                            }
                        ]
                    },
                    "bn-BD": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 38049948,
                                "from": "*",
                                "hashValue": "c3a95d03fb5b0665d05bd954fec96a140091863ae75b982170bc47f4aaa9a26db9244485aa4250366a6427cab5851d7c87264e2ad8c1b9e7c799934f1c08d8f0"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5248007,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "bec5bf5980f5b316d6bcab9345b6d430aba0e6a455efca09e5217612cebab29d20d9105b703695fe7f73be54aea752ebb8022ff7449a3b5deaf27489481e1ec5"
                            },
                            {
                                "filesize": 5295083,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "2cd9af6678e1a5724c87303e76a467f59a2fd3223f4d574853d2935e1ee414ce4474bef2a8864f1ec1b206d1925138ff8e0be106a718644dda6eed671e22260d"
                            },
                            {
                                "filesize": 4815579,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "f1ac066dca69e29792af9efa79f1786cb024995fdbd0abde4ef0584cb65124094756bf263234ebdbeee66440a1c3c55448d0b001207a3a27a9f328a72cd2c33a"
                            }
                        ]
                    },
                    "bn-IN": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 38044652,
                                "from": "*",
                                "hashValue": "f418a47f3862abd798921d7d9c333b0335d140431cf6a153d44acf522da3fe3a7816b3f1c8b97799919e71ccdba838616434a749c636d3ee2cb195497534dccf"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5248015,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "8d597e1545445312c8b3a9cf5c83797412928c3e07c5f7cd7dec1ef42df932d7ebae075ea0685c24d7229a4bae2ba7936df355b54d5c8a052621f59d54a35d8b"
                            },
                            {
                                "filesize": 5295075,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "f6dcbe253a068dade2485935c3b5f1fce45d749a17ee03168a7714c33890e6344d446176bb109d9cf28389dab2df233d19687fe453ee018f450bf874b7628079"
                            },
                            {
                                "filesize": 4815579,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "7a17f4c8c00d8b3db62109316d1d7a716918b94be4661bed02a6f1f41fece86f36dc9ded635229b10faafdbfb6919dc8e770be5b66d92ec730f6d80a23e31266"
                            }
                        ]
                    },
                    "br": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 38743488,
                                "from": "*",
                                "hashValue": "ffae630626195075561dacfb5b02a42b2a893322ad1368c2cf52cbba79cb64e955a4b8154706852f1d001ebc2443b1b9372d24df11e715def105b680b8ad24c8"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5247991,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "448b7bcda401e21157a75112930b4311d9b9438f4459a57f7018bf8670b8b721b0804b5b21a541a21d65aff118a712f6ee038b0628d0f0afeb5d406fa364bbbf"
                            },
                            {
                                "filesize": 5295047,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "e08b2ca9bf0661076b0ce3293642a08f2bdd003fa052be5c083e9e43420236ce173a6f84e77191d0b900f82bc83494bb5f501a66306b244e87cacf204d07236a"
                            },
                            {
                                "filesize": 4815559,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "5e2db5799f6155c6ea03d3ff5cc7a8cbbaee31af548810aa3f0a9036d0f714ed8cb89ca620192ac0e2e6d6f233e54ed91bda26979096487c76ea00ac84e8f175"
                            }
                        ]
                    },
                    "bs": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 38035228,
                                "from": "*",
                                "hashValue": "03c4478efa7bb9736bd863f809da59590e7688c3bfd6af35a7d5cc0c87ca00a0b7d300676dde072f15a9f9746cfb96eda3bd1aae4a74b9f0ac3174591bd17c5f"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5247963,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "36f0934f9b77857223f46ab8bcb8cb68e1d50fa675e733c534b8552502307bfa16eb475795bfa0e1aff5cde333368fd52b346d065f28f6f8f90a1950866e5efd"
                            },
                            {
                                "filesize": 5295027,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "cfee9594814cc066e807059474a883fdf209149e467d0297f6c4ab3c20ddc7255d3135185e605aeea5fbcc6f5c9843f9af6275a42d73ea1c6503329d6b877fdc"
                            },
                            {
                                "filesize": 4815539,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "16320eaf38c81a8382d5db0fd3e99546bd7a093dfc66c76df7f60aee3d5e30c3a71ae5fe1649a23c6d1284feec9dfe03bc637afb4588acb54cd3511e689ff3c3"
                            }
                        ]
                    },
                    "ca": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 38361204,
                                "from": "*",
                                "hashValue": "2334a67c59238bb2f71db309f5d55428bb6d5a65c4d652986bb4c1c5096739c85dbaac41af55eae4b4e6e85685022bfcb5fc2a9b10865da0e59f361ffe445c91"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5247983,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "acfdb01c05a0ce0ee3bcc74d004f770a73f64010a03c7b737c006ed532605aa1f0089088d632f8fc80b7ae7d373d6df9c36cc60e0ee633202f3f71cc2c3974a6"
                            },
                            {
                                "filesize": 5295051,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "3c943bd5d621fb2cdc844d2710498ffac33a99b44ff2352e55d4bc10351c671732cc011ff1301c9f7bd4f627d85888b9aabda50d9907a72c648131a22a80b8fe"
                            },
                            {
                                "filesize": 4815559,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "dad5d3245cf1d4c5850d5d74a50f54ed264cf4e731c49772de5ecdadd7a0ef7812183e4e8096c8e6678b60c5ee872deb6fe619cf578470683ab29897503c1cde"
                            }
                        ]
                    },
                    "cak": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 38039364,
                                "from": "*",
                                "hashValue": "9bdf41bb14991882a1cb3ec00abc5569d1d2cc2c03f51e1440d667a88f7481c90b67e1cfd443853b74cd21ff3adcee6b815987b05527ad48bbe187862a081263"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5247955,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "054e2f630c5ea927309d26de2418b16d6aec611e54422b191d4d24b2fcce45eb9d05de299cf07989029b7c1e25f7642f55fdd1aec92d49e61a0c5217e502909f"
                            },
                            {
                                "filesize": 5295035,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "954e89d9b40580bbbbbd7c1ac870f1b28563a9925c6f852339e174f987f6db924910b27324c75df2ecaabafbbe8c27242d6b77751cca48e80a53ba8d430e5102"
                            },
                            {
                                "filesize": 4815523,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "e50a2c5ec85e367aef40e8c022d3b804c25768bae134058a311af727fe87947c38690240e3ea1eef8dad20865ee2c2775557e7c1524b0b441aa9f4fa439264bd"
                            }
                        ]
                    },
                    "cs": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 38034904,
                                "from": "*",
                                "hashValue": "162cb72446fd2a3c123b2a9ef1eea2103b8ccf6ce2445c46ee4590bfb4457f4c86a35803a9c6431f6f311f8666b2b868c79fd6779faf58b9c9a6ab139cb74898"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5247971,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "320ac4b9a51745cf32a448f1ce56c7dcdfd8f5ff5d6d6eab07dd38c58bd3bb5d45e41e1a9cb230fa088bde967362eb699a16cd3a9f7fa76d62198b349f8261e1"
                            },
                            {
                                "filesize": 5295031,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "c7d7ded299876c8430ae659b86577d714f7d03b6fdab12d45dae2ef0482c9e5a734364b1c4207fa48769f3a186d3696d3efdc6aef30a0008983f88d940b5b896"
                            },
                            {
                                "filesize": 4815539,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "c3c1c2720a64290f19ad4822486a27119039c9851eca0bdca64c749c2c048b97c6f4344101502123559d13e488a74891da3b787bc42ca7d0bdea2add748da80d"
                            }
                        ]
                    },
                    "cy": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 38030852,
                                "from": "*",
                                "hashValue": "82fb43663b381b638aa6d67bb1eb99765374e89c2dee71671bea5eb461d858bd6934c0e7c06880f820e11dfa47832fa9162a0f6c64ebd390cf534be6b890728e"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5247967,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "af550598f1f2cf865e0687410715ddb8b0a43d0762f9305d7f1d704a26095fcc669c4d26fa48556ea710ec0561f288977f6eddb79e55d6caf148ba67bcb81adc"
                            },
                            {
                                "filesize": 5295027,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "ca27309cd3b2bae3e5582bdc89ae6616a57370906067ff91315c8da835605f068f307ca6d40851e57c692509e8cc40e6c16145f57eaa97b25e8b671c088c76f9"
                            },
                            {
                                "filesize": 4815539,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "567cd02cd0d1dca9642769112e024c246e237cc4ade121f5fa366f0983cee2b8c809ded43cc5f1c741090ada88c806f88c73a293591d5fe5e76c470ade9a76b8"
                            }
                        ]
                    },
                    "da": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 38539896,
                                "from": "*",
                                "hashValue": "7908f443621e2e9b5cc9efc7bb0495ff5de3c25d0a6f679598fdb87cd6462002fd99091e2b91d15deffc688297fe1f42962670caaf2b7da02aaf89fabbf0b6c3"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5247979,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "cdc03a7d1d4ce0f7eaaf5d9f76da0c8e27ab5b00d13bbeb69ebe5f6ea0c1b40f1537008f146ee9469868f3b2802333d0e91b4e284c125e36eeaf0cc90ab63ab3"
                            },
                            {
                                "filesize": 5295043,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "487da4139e51c09ad6e2ba99b3890dc69cdae996c930193c20072f0119db2472962362703bf1d57ada27f26f71a8fc88783e8585cf96900255b38077baec036e"
                            },
                            {
                                "filesize": 4815551,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "eb858a6149ef78b856d143ad96d2a9b4ae5f4e289b5731a52bb524a85b70c1971cb5575141d143e203b358a8813e97b99509d440a3167edfb69c92d523482210"
                            }
                        ]
                    },
                    "de": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 38033732,
                                "from": "*",
                                "hashValue": "0554f91834e9e5be9cd059cc266ce67b4a5f19a62c747cf34bbb7709b68c4afe1d839e197703a8b363e5502808f626b91ca9564030afe31237d05b2ab290c321"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5247955,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "34c57c95501bcf9e9b738d12d93c3524300f30e6a203624ff491a79c6979685bcd47f45f4f6dceec91ccc98e62e15f9cf04c41ced532bce11b41e686c9f546f7"
                            },
                            {
                                "filesize": 5295023,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "2cff1a9264c4c2262f78ad310d3f0ac49b2f6302fe07f1f3bf390f7e37e7084d9cca86c3f310fa69a9da332a8b982081c23e4ec0f2ae1943200f8e63946d6b46"
                            },
                            {
                                "filesize": 4815527,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "855225eea9072ec73e2109e42fe022078c2b4fe7280606a4749d40fb0c759e81c82825e59770ee1c92c7b9e87dfffe07b53dadc1274910288cb37bbf62e195b2"
                            }
                        ]
                    },
                    "dsb": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 38039028,
                                "from": "*",
                                "hashValue": "cfb3c6b26532d07f5f78f72c99ec2680a587aa2d13a28e360f1dc89f18ad0cbb5153f0c1ae634f00a51b1c9fc22e96a498f0a0bb0b783fd21af0946272af7043"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5247991,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "47bebd7320090dae8880aca541de60d0528bc3e0ae52efe47878d2d34063173dc2fdcb6b2fd5a878a42a93104d7f78852e0a49a4638a0706dd7c7b8ea2ff91cf"
                            },
                            {
                                "filesize": 5295035,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "e36b009795b305ae7ce22c76cd4cb7b6af9496408cb984aa5947d8bf5e8d4eda29259044b07c68575c429d57549a144231a0aac5288b7fba175a48f5b159a41d"
                            },
                            {
                                "filesize": 4815559,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "4b506682d46e4f867938c4f7f19a87d27e08611ff88fc31bbc38873b818ee97c05a3a6a4c10f59d061ebff6f42198511dbe73bb86b9581df91b028ab4d186c88"
                            }
                        ]
                    },
                    "el": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 38052880,
                                "from": "*",
                                "hashValue": "46a1c34ec5488e0b1a5d866b696982ee8c4e66f9da418ae140501fe61565d9cb15903dfdf023503454673a912b9647f802e12c07403ed0f0340209aa79e039d7"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5247991,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "ca53db6face6e679c10e61cb83ddcd9891d3cf9196543996f740caa257f651472349834612650560e7d668cafe47aa2007a0ccada3b67602e470b6719ddbae82"
                            },
                            {
                                "filesize": 5295071,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "5ea83c87d5584d1dee188b81fb9961c45b39d4db30f96b07e25424bd48f7c35b53439a49713df5576cceffb91b805732c5362941fa8918aaaf1e998ba211564d"
                            },
                            {
                                "filesize": 4815563,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "9c93ecc851304cf579fcad4f62280e991ddada1895f3ae0f952e4860d7562d09af372895b4eca021e6f621da004557b0736422d0fe30044eacda531f67a954e5"
                            }
                        ]
                    },
                    "en-GB": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 38013664,
                                "from": "*",
                                "hashValue": "61c567292f35847dcc2732059c6e22ad4838ef4d9c52f38c3a8eb8359678ddff0c8bd94c37e9162ba7b5e7d9de9acfb0acca5871b0ca9ddfa5bb4de1659b27ae"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5248203,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "2aaba50a13bf02bd19a742d4d392faf4d5f2378f0967cab9e86217336062987b63a3402720a04b92e13ef95084c8f5fe8596fffae11960614ddb5913a19c2cf0"
                            },
                            {
                                "filesize": 5298691,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "c487259a8e8dc9424466d21bd37190ba68347c8fb46f095015ea2e9f78e593b583cbe88a891de8ef57c92741699cdd8d6cddc8220e5fcfa8d82ffcb6b4197da2"
                            },
                            {
                                "filesize": 4815779,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "fad01b80942a39e080f8b7c84ba515a599095f7693648a49e534848155fbf179d50a29b9cd1356292a7478523bad38baa93cf43d9c945f23d6b3f69fbb18520a"
                            }
                        ]
                    },
                    "en-US": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 38178958,
                                "from": "*",
                                "hashValue": "dd65ccaf3357a0715dc44f92b02da7a72ce5ba2222b56db5a721f21800220bad34b8f9e76881e5be66d64587474bba7b56585db3798360235665339ca715b3b4"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 4815547,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "0398947cf1438989c078d26138a995841ecff8f9f082f5db605a2f9f4765f4cf7674ccca9de0d0af214e718d62ba5393943131922b509303512ea8afaae55fc9"
                            },
                            {
                                "filesize": 5247979,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "07e888a13224c0aa4b2b37e569fad93afafcfd7f156985d8bcf5c30463a461a3f0d0cd75bd146fd1bc4a2f5e1fdc3bb8ec79f80e2286f0a9b74656838a3be3e4"
                            },
                            {
                                "filesize": 5295051,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "811621c184b18a66d86019ef7341c2f14001b1874a398d957b62ce22110aea7491565475162b081d70ff77b6500b0f4af1026fac094e2419b00edeb74a3a2088"
                            }
                        ]
                    },
                    "en-ZA": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 38011524,
                                "from": "*",
                                "hashValue": "1d6e8d716f97215f820f17eb7da389885932fffeb4c5d5b5f8e649763590b3eaf12bda61ddefdd0b547d3b2640e5f2eaa0ac426f85a6edcbfb35bf01fe6f2863"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5247959,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "4b796eb7319b580e3fa3b18790ca90ecd6343498dc0e3777ec2b99c965547549e5c5327480d2ce7e2ba07bfad374478ea513dad5a9e36a39503cd2605f9fdf85"
                            },
                            {
                                "filesize": 5295023,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "0eed8ee59f14b0864a170780473f0ae8fb2431b856d2f7da444389462b915c0ebef744785b7107a7354ece15cae8500b676ccd70841afd31f2af37807711c179"
                            },
                            {
                                "filesize": 4815531,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "8c431c495bb2f02b9e03fd2e8ad6231afe6742606987babbdbb5156d9a011d88a79cdd54be5fa4a410d7b2e95e6b15ad3d9c07c11e26216cf8d685f3561346d7"
                            }
                        ]
                    },
                    "eo": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 38029532,
                                "from": "*",
                                "hashValue": "b21015ff109f7e90a4bfb65b957f4a74bbb5ce99394e489438c0b85fd60179dbd72203822758b673aa0e7dcf23028f0742ddf352c4c1315805c6bd8ad4c2b4d1"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5247975,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "fec0ce99cee4856b624c6fa4a0aa6282bbd0a9807c6632cb97adb6ca9afa60e08c9b9ffde01a450269ef3419c7f5892cd6fcb9eb0c5d79792e5298a59345b186"
                            },
                            {
                                "filesize": 5295023,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "9f0272c1b37f9ea10e6e132dd50f7244aae9054fd90cae6f1a2b068e16ed64a45ddd8f59644601c470c8d886e4356bbe82ed61f8bd91b19967659e6b8a899fc7"
                            },
                            {
                                "filesize": 4815543,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "9856619e050f7a436b51d33d0a4046b8c6c3ee18cbdbdc3dd1146defaf493b2b96385f3138f5512c7dc1120c48753e8bca6f6d46d7b9d90779f05b7451e2bbde"
                            }
                        ]
                    },
                    "es-AR": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 38034260,
                                "from": "*",
                                "hashValue": "09aa8bd8089ff86243d0bcc80ae5992654a449b78592a5abb3c47c6f9e708d0d5db4d96708d77d8e979d8db597c4c9a75283da4fec39f11775cbf9fe2da151ac"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5247963,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "8cb9851e1a820519653dc791c162bd363e15726b7412883a93fddd326d57f6adf9f3882ed202040e72231d65f9816c6c677851d172e0277410fc64ff7f1cfdd2"
                            },
                            {
                                "filesize": 5295027,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "29aef7e3efada76e48b306d172caf17e50d91afe1c5b89043f840cccd61ea5f94619b57004a9da293790245ebabc70162e6724165bac3562476b252daf9846df"
                            },
                            {
                                "filesize": 4815539,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "10f61eab0e7cbe4890b417c35fd66b11f6ff5dff200b466cd3578c1e4f3df554870bc76e32f1b5d5cd4b6d2eb26a5f7cf30f56c1591927549a0fff2444b9b96b"
                            }
                        ]
                    },
                    "es-CL": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 38035856,
                                "from": "*",
                                "hashValue": "07045b7687d38b8336d3deb138dc8b4a4f76c17bfd864ca212efaf9c4a48b77b7511c61719e5f614324d3e6dbed8832cb6fee5a4c071f48bf939838e0aa42138"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5247967,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "6d49667734b16b80671d396c5c603c02e4da738d60ff477107474697d77fdf65a52bead15d752bbaaf134d79500a4fd0b9792517c29760ed736d6019b5e22136"
                            },
                            {
                                "filesize": 5295035,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "05dbf2bf65484fb69e20537aeb26c3302a2a8c30285310026598e82b0010c0fbf41ede278250a74d725130099c53bcd478b1f9b4815ab6d11e90d55251de0385"
                            },
                            {
                                "filesize": 4815539,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "48156e457fd22f2302ded5049dab71b94c3cbe806cb33234c11cb8c83ffc8716e6c6faa81945d36c7f30c014c81168498547be4964a7d0e55f766447d7386851"
                            }
                        ]
                    },
                    "es-ES": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 37960752,
                                "from": "*",
                                "hashValue": "151e92343e9d30769b944ca0c72abd1890a06a8475c544cd1e0feeb7c9214e04621a89571d33bb567ac7fc1813ed5a891cb460fb20202df458168a2d80581e97"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5247891,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "138ef9572e84d7a3d81c0fe4c3ae8fcaa8e2cc9ee4be68ae6bfd67a61f5c69cdc8dddc31213ce212e0c365a923a1c75b8eb634e9bcad96b0b0ff64683c43e20c"
                            },
                            {
                                "filesize": 5294963,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "6e406c756ab9de65483d550078b18dc2d646797ce96fbc33d5c9332da03720bfee1b353ef4ae88b98b78e51ca36eeb8464036efeed8d17e58db4ad15940955be"
                            },
                            {
                                "filesize": 4815467,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "4ec5fb8defc368ecf46fc497b76b621a0e7dac06fa117915c9e1a34132e60e9f4744d2c1824c09dae7bd5872b5fe76fc6a170cac25f52366fb6f77793c8dbb86"
                            }
                        ]
                    },
                    "es-MX": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 38036796,
                                "from": "*",
                                "hashValue": "7bbd5b810828176beba98161bc76df171c027f7dd82ad56120e13307cdf5d9780c4a1386c37ab913b4aef1a15152ce593fd84e0403efcf3f72c1a8b6f1aad7a0"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5247955,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "1b898672d8e64b198316d417fd58f17620701d02752cc48972a46332272c2d26aa8c066f08c0c7faeeb19a0b1d07283ac681fc068ceacf4dd104b8fb689b3281"
                            },
                            {
                                "filesize": 5295039,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "38aab8fac4cc9dc9753a5c34cd60143393c7264a7ed72e7d9418a0f34ae82b87b6b9697c963c3a8ecbdd7ae811db95c69a2dd1bcde8c70b9b48526351114b4e6"
                            },
                            {
                                "filesize": 4815523,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "ec300783cb72022556dec199829c39e7229b03b85713a709b01b7e950090f6bc8261e6527b8d139fd896230c08e212df8fbed2c5f9785bb76c7e0bde77509c8d"
                            }
                        ]
                    },
                    "et": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 38657608,
                                "from": "*",
                                "hashValue": "7f4e44d92296826b318f44fd55e3cb6d17d322a24fd6ee7feb1ed15992266b134f0f3950037f0a360263bfa98d3ff8f17d6c11e9c08e7aa17639c67fbe92acc4"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5247987,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "ca3279c977489465b92f33b0e695d045839183375bb1059564ed1cb768d8d67a6acf96ac271ae0be4b586450fb8e9625056f15b4ff159b3d7f55c72a4a2702fa"
                            },
                            {
                                "filesize": 5295047,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "108036239a9c232704c24aa61f7517823a3dc329e47915a6aa925e05dd728f828223dcdb87904f8853b6df69c126cfef568525e241aa3e53cbc561ed3940dc4c"
                            },
                            {
                                "filesize": 4815547,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "4217c4e39fcd2738d0c0f50eb8021a1ff740b30a14fa250492ac4c0eee7c5acda1145e1b0f398f1343dd877291ad1de85668a272175cc4efcd98726b4d1e90ca"
                            }
                        ]
                    },
                    "eu": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 38031608,
                                "from": "*",
                                "hashValue": "c5897e9401623f91916b9d737502570d7c78d90338556903e1095cb44faaa7b9604f870e2f8c9d4421d615d9c95ddbfc2f079e966b1ef82a66f5fdd7ea271592"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5247959,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "e390a9d41f271d1f96a2f912d3f14963af995475d95959a34e41e631434f4148be660421e41b8f0462d266f1dbc10760b79197b5a1c7598412966f821b90604a"
                            },
                            {
                                "filesize": 5295031,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "3d79da50b97e4e53033eaaceab86b71523f5fc5c34f4d8d0a6db90ae71dba4a3603ceb48be08d2730342ea2f5ae92a25f29690efed2a59be99917a11f2279b0e"
                            },
                            {
                                "filesize": 4815531,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "716e2f4fd7623dcf1d666c894553d86a98f3f4e4e16c0e8295038ae71cc62543917490b973f55efa7e0460f73e5713f702c303cbe1641af734af122f24cabb5f"
                            }
                        ]
                    },
                    "fa": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 38050868,
                                "from": "*",
                                "hashValue": "9e442129fa6ef9d7891aeb767b1744859807b2ffb8ce19cfdb457deabe10596d90b73f89c40e5e11f62f708b8fb3fc2a9fa262f47eea433d4d9919ffd7eba906"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 4815575,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "b361558d89b5d9adf2effd8950d390df54565460c43f31b47f51bae08b142527e41cd5afe0ac3bb3322020bbf74e97b89176e3a37ba4172bc4132e02c11c8531"
                            },
                            {
                                "filesize": 5248003,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "a278c3136d4fb82be8f1026b68b2be12e67e466f0811947e349bf2fac58b04d9202113d20e5bcadb2107f87bc515d845fbff99d45a4fd2b51c0ec5c66899f6fe"
                            },
                            {
                                "filesize": 5295059,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "e72c508947240883d3fcd770de9e6e69b5711f03b49c834b08ec10e8da9b48602d8c5af45b786027a8f75c6950c7f53f6e61a352c3717bdbfa55ddd881209efe"
                            }
                        ]
                    },
                    "ff": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 38031840,
                                "from": "*",
                                "hashValue": "fda1332507e5ff007d3d4766baacc0891926c1226084f62c4f621f4a223f620f5a18644d98ea4fa1b51673325fdfaa17854c258fdeb1e5a5ba295b20e88e6a75"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 4815527,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "a8d821a86cebedd44363b95c4fe9f669284b4322f5138f00f922c5b5546731e20ec575e97440e4d808d4263e640b1cb303979436d7cd756a1812572e638019d5"
                            },
                            {
                                "filesize": 5247947,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "a44acfe0019639e6300f29d55693b87a615bafc57f19046c7b9f04c1b9bb5849ba653e183235b6712861efb2f3b8c50b6f6b0a6cfa749211a65156bf486cca3d"
                            },
                            {
                                "filesize": 5295023,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "9b61cc2c123628e342b2a66490363c780faf3eb7750477085845ad8bf5f56ce1940425b7aa236c057d36558c52b130a11fe9fa582b688cda5faf67e012cbd09e"
                            }
                        ]
                    },
                    "fi": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 38026824,
                                "from": "*",
                                "hashValue": "21f7b920f245e9703daab9c3fba72a33c4dc0c099fcdde2ccc11162b969244ecc0939338594ef8f89ab0344bca30f5f893939ae4b610a3eae6127691c8aa9194"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 4815515,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "83e40a76c916f92dd4aff54dbfa5f81cf2ec23859e62d73a29583884f3dcde65cdfb926456606b6945ab58637e321d6d6ccbddbb521714f571effd1a2f0e94e1"
                            },
                            {
                                "filesize": 5247943,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "e764c921dbfae1cd7f11de3a2da46504c2af39afe62a6b56a2b05a0a0eae788d5fa15e95e7dee8a30f4cd6aa187ad94009a3fbf98bf1a07c5df433d11d3a076b"
                            },
                            {
                                "filesize": 5295027,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "994404fb8d723fb7241014419c6df6a1b1ea603c0d3275ec982ce6256cde824f9ed059b40be9825e756194f3fc064d29375219295082733ee829af2a06f39f48"
                            }
                        ]
                    },
                    "fr": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 38321820,
                                "from": "*",
                                "hashValue": "639e33ff3b8dd8632892fd2f5cecd72fa64da82e34f1519350dfe7452a5c5c3c9b2f2031d4e35eea4b2ca3f0db923688c21984b056a80a749bf06398fbc82535"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 4815559,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "ebaac646b0affa04dbdaf3c177a3b439c5dd317474775ac622115e464a01fb3b89c0ff9860460d13b26ebf9f6007e7de7cb8f68f93a49c8f1424451fd6d43273"
                            },
                            {
                                "filesize": 5247987,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "055321a2405e2447a5756c24b385570af006165292cb1d617f930256fc6864a46c382e40cf466a7b97d469df288ef62c361caa6d57bed54045397610300b86b5"
                            },
                            {
                                "filesize": 5295059,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "a67db4ba7e7073e25f294416851e03e977a324cdf03c32fc74e6dbb63daf71fa12d9550a3073044823958c94a4ec6a74554a9f8bec79c6f99f4b2b3986f87784"
                            }
                        ]
                    },
                    "fy-NL": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 39321090,
                                "from": "*",
                                "hashValue": "a27db34a6c0a6bfbf14db7ccedbfe9b678b4485c56cba35578897d17997c46d5c950e16fc3ecc75801336fcc4dc3f4e0a64589926307957fb3b9a925dc063077"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 4815551,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "b4f062ebc0e6f8c21b94bf48bf9510566047b8bab08a42483286085e2b6b429fc14fb8c725a95cf7129cd6fc4c31912e24bd125fe422222826820cf876bb0120"
                            },
                            {
                                "filesize": 5247979,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "6f9869a2513140f6829d2d4a257801b93e40544b2b6f2285c27d8423535d72548bed4e2aef07d4725e7f55e87422c6d0d68f7c56063d9891a0889a55ba62637d"
                            },
                            {
                                "filesize": 5295055,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "0d89aa7fb274a925ae715dba1e818a0cc22ba1bd34e19ae7550d205f0aaebfe7d239000edb72088ce7ab2fb12f538e598e081f764813b0db49230e7aa581f9f8"
                            }
                        ]
                    },
                    "ga-IE": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 38039508,
                                "from": "*",
                                "hashValue": "493099bc04ef2c2761654371d6c42e004b5f91814f083e563a66109646bb6add52d789a84e2d2dc7c8d4357f12ec84533533c5d770a61124fb58e1379140bca6"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 4815551,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "b202c8ae6c6461be4025efb9bb6879326987ca17f1734dba1102fec209f69d60016e30be57af30b7ee1ac7486949a306ccfbd93f2f2464ed1de9f4e687408fa9"
                            },
                            {
                                "filesize": 5247975,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "66413dc8d5ca9ebda338fef4c5726a0d7bc852cc9c9d7a00e10e8b71106d309066d7aee6ea5ca5b59958a2b69ebf2f81d145c89fd982d91e6e2a59d3eca4664b"
                            },
                            {
                                "filesize": 5295035,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "196a014c29fcce9aa8a53ca7cee96b0b50cfa3b872784c082f8095bf6790becee2980815041ad9170a94e5f0aca5a2e01195f40b2cf1474386aff01edd18d9f1"
                            }
                        ]
                    },
                    "gd": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 38033620,
                                "from": "*",
                                "hashValue": "8f707bab3a3c46f1a58c4d29e6a21ae754f95375e335bd4937c3c7208cb0292044fbbaf3317d4d01a5c5ad4ca3393f883cf89a95044e1ad955536fdf9c1f905f"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 4815543,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "1232a867916246b1ca516d7d44fee4862a417ba3bb6dbd9fb4e0a9343c6b9e0619ca8417c06fc42aec91c72d682b9d0d2b8ef219bc3cc42ce2d8c25e11234569"
                            },
                            {
                                "filesize": 5247971,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "832f27014742f9ff7abe8775b554bee82d2f92b4d40463907d63a56543fc2b0ad3769ee30ff0280a5946b981c9711b79fdef3eaf6cf180ea9807ee3f16a4441c"
                            },
                            {
                                "filesize": 5295035,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "43d40621eff1eb032268a7c0be6f13af3ae9103b0b9eeaaca7ef1b389788e9320035e08ca77f33bf57204fe0768fe58550da76ec474eab6a1314212e2790e378"
                            }
                        ]
                    },
                    "gl": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 38026184,
                                "from": "*",
                                "hashValue": "f74d80de881573f1544ba7c8e274633beb9541b78d9d68d2ed1bfdd485d2e502d71a42c7749f675c46d5f2d167acdb6933476ae6dfecac79b79e270960d6b07a"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 4815523,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "cfce669d6ddd80b00040212920b5af9ae6bdf714dab0a0e4eb7cb43b9fc8c4534a66c7e4e8b594a3b3c1f958ad0821b93ad2f112d02e38e10b945f07ed801209"
                            },
                            {
                                "filesize": 5247955,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "b2f237deae7aa9446c38a8e0e7db801fd1a9c7fe2356e7051c13d562877a872e426950e5b140770c336cc5b8d3b067b6047780555b8821247bd21b879b65b629"
                            },
                            {
                                "filesize": 5295023,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "a6a651960c4992e790e7eb8321a9b7f88d811eaeb25798a0846b8b4441df0c358e86e9b6c6f9dc134c96ce25999decca38bcb313b808e6ccbde93afb4bad8ac5"
                            }
                        ]
                    },
                    "gn": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 38038084,
                                "from": "*",
                                "hashValue": "8fc228b8687ba917cfeb6ee6bdd456ce21743a929c052ecf92f67cc13a4f69c7443c33604cafca9081f11efde7f4766001e698981106c98748717d764c6911d3"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 4815547,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "848cfa9013c1999027ac9ffeecd2a0169d647a3de68a9f0287d9b211c5c8f307fc9f35990aa2a9cd735b15c05bea933c1c15bffbae933ac2d62cc638c07a0cc6"
                            },
                            {
                                "filesize": 5247975,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "848acd1cef9e4a6cde9da4d292e655ea4f1955d87f62eb2c2b0420842af5d9d8b550296a0046feaae08f08872d28677f0ba5637ac628d0fbc3d3cedeeeed6485"
                            },
                            {
                                "filesize": 5295027,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "26e804de4ef608af9bc872bd39baa6c8fbbb75aaa18fdd0178a8ff4d68d82751c0178b590b9eeb346f8d0636d8a2db407b511b8238a7c77bd224048330726d2a"
                            }
                        ]
                    },
                    "gu-IN": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 38044480,
                                "from": "*",
                                "hashValue": "89286a2e668e618a7609c1e63d761c9239defa8f41630e155d1bf4d50e3cef40b1fbf5509417de1d6852e97c45b2a1dee07910646d26e6267edbe72cabf71857"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 4815579,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "262af4cb51630ef94575169a75b7c3c31e390967739dada4008777f8ab2ae813a3d2b80cfc5c524842c6e0e8586f972f5585fe505d2c8e80b757765623986376"
                            },
                            {
                                "filesize": 5248007,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "eaabdd421c7898ea4d7d9d108031c042d4b87b189970d8c17a4e611a95d35efe869b765151c6bdb8d8c30eecc762f8ac5bcce34a818b94069e69ff43dbbf22c1"
                            },
                            {
                                "filesize": 5295075,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "582d6259b76cfee08612874e2413ea064fca6c7b7af25f47a4a37b5d93e54527c3fee61082dcc2d568a4ea425e3167541dc0fa6641ef33aeff14ef6d6236d7af"
                            }
                        ]
                    },
                    "he": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 38035524,
                                "from": "*",
                                "hashValue": "d66426c48170588afdc4732489c18cddaed6523297eeeb03de2732104766baa63739c82e827f5dbc9bdadcb7c0c13b8adee2e8095135eb865e19ec83d004eb70"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5247975,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "30b66cd6a7756a9a0bbfb2f399d17ce86d34e67c0d9f075e4c78abea8f2b9f227b9111ea168e744ff4622f84dc715534a75a2effb148773a03e6c3bb5a5e1e54"
                            },
                            {
                                "filesize": 4815547,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "bdc1950e6f5c7bb34d848cb020754f602bc72fc05fe3eebf74cb16c0567ce75b05e7e82ff8d12b3046f725359a74039e39a93e286ef4c9498f9edc819936a2fe"
                            },
                            {
                                "filesize": 5295035,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "7df71b9196b7a9a2ce38b9c8c719021fa8e4e518830abbbdb548d1bb12251aead36e5745b2a4f9e44c55ff17db589fe1ba556a01597b7a7d1827ce1a5d8da092"
                            }
                        ]
                    },
                    "hi-IN": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 38050408,
                                "from": "*",
                                "hashValue": "0244b1ccb72ec1d4a4134be4ddddd30abd5e71fcea1e0902578e8e513f1fe53d1600285905154320dbfa85ba1381cc78bb73e58d02bf873345280b51c33ceca0"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5248011,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "aa2f2d74a8e28c5774568627e4f03b1027be96c57112166e021fc66880ec0d416acafbf94d87261fc6354ff1e3f3c3fffded8c24162d699aa13bcc446886075a"
                            },
                            {
                                "filesize": 4815583,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "92bf3a07712e0efd490c01372cc0464a6e709f6c2ad779af1bfdcf9c16e990c5beeefb9647f8853d39f75dbf60f1311b70aff1b153259737d937544290cef538"
                            },
                            {
                                "filesize": 5295083,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "35d3edfb54a4c4be870aa17fec8a5661360c36f206207e5c64b4b3c0d5ea6d1f4e155a30efe040f5544b9c320393632d30815efbc90ba5c0fb826ad79dcf8d27"
                            }
                        ]
                    },
                    "hr": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 38034452,
                                "from": "*",
                                "hashValue": "3ad2d3789481b2262f6e37ca1072e19cc5374f3f2a7675f70f384b81357f33ecb0387249742651952808cf4ba3922773ed8a16e7a4b54e756851b25731b24fc0"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5247939,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "f9d206f8e28581b92bf58475e9f0b27b0d50c4e9996ce58252c05e17497c2c675a568e91cb3619b4884e692739349fc67a01b5a3b042681119693e383dbd46b5"
                            },
                            {
                                "filesize": 4815511,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "c9baadc0db23653c53ce2e036ccd209e235d6603eceb6af16e424b154ecc830791de92abb36ed15d8d38eb408572b13e6c9fcadf72f99db41eb8764fc3cf4e83"
                            },
                            {
                                "filesize": 5295027,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "4111dd1a86e1012758257e56546b84b765759c2c68ee039d887bc7a12ea8e691080cd055adb457f2204dfc3264ebb8a0ffc513d9af31f5f518e9a4d4f0a7dac1"
                            }
                        ]
                    },
                    "hsb": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 38038568,
                                "from": "*",
                                "hashValue": "c3b128caf4a9c9f46567fe236d27c53bd55b669012dcd224b1e5d037bcec57df954b36adb19de735c0e58a8e07739d88c189248f86fec59c18331ecba156afd4"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5247963,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "623ddf18858bc89ea9d55107dd458d433d766f5f3cc9234379229e051a9570211cce7a34ba8db131ba0172fb3bcc1b03a02a1eee91a97c0024dacf2164dd696c"
                            },
                            {
                                "filesize": 4815531,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "3cb4e66d3467d6cee23a7f58f43bb267dd1dcb0665ec5a13f6006cfe36443412743dee09cbdc3736d07064868cb5e2630c609fd021754261e905b7ece240fc60"
                            },
                            {
                                "filesize": 5295035,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "e6dd554e52a8a8496ee054ba79fbb238052c3b1d8b121de4489801a98d2d71c537e666e035c5defe683239b333eec25e8e6809b6f2d3238ee05d796d2e0c5046"
                            }
                        ]
                    },
                    "hu": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 38589984,
                                "from": "*",
                                "hashValue": "78e2e9ec2acb5ce1301f4e2409f67666c2166951dcd623b5d2c0ecc34341983b6e4398fc0df10167b6415a37a37330f52aa6ec7d0b45c96a789575a82e07ea70"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5247983,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "9e05ecafe44ebf242e35e2206a1b3bf9ed50cbcf5171f8ac7db81c50171e5e44ee8791342637a021a21e95fe99da9effd5e121b01faf81a6e642a8fd6a8e1d62"
                            },
                            {
                                "filesize": 4815551,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "54d2b96ded6591cf89b49d55e0ce3cb8bbbc52e78d43ce17b5d6c9c8831830586b7b1464b99c9fe0c589776eba81f72512f219b253845e137e18cee9f0907e67"
                            },
                            {
                                "filesize": 5295059,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "9e459bd20424e0da750eafa9040e6950b9da351f90c1e1ad2293215249db403fde24f38b2a53070c3dc0a897b166d32456b82bbf8c5b5989ede7020167c9a6e8"
                            }
                        ]
                    },
                    "hy-AM": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 38044352,
                                "from": "*",
                                "hashValue": "058d086547fbbb00334874276bc528c27518ebb91cc49bb2ca2546006b872d61a06c02b09e3c6c5823f9701044aa31a0f01381b2e48da22dd7026c9f31a42220"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5247975,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "82df4d3657c533f849652e827cb6cce7accbf6ce4b1fbd18977373019051f709d0e8bd6f873317a5870db9e82eb9c8bb9e7622d5fbe5f6badad61e0f501d20a1"
                            },
                            {
                                "filesize": 4815547,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "c8b6c47cf48cd180f2ebaf014c6bd0fffd5932ae73e0cb31fec6b1163c6b4650842035cea409a5742d341874fc9677dc5b30c8cd33bd1abdd209d1e89d72c3fa"
                            },
                            {
                                "filesize": 5295055,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "36a51c6e2c0e06116b68d29ed9cf668a6daa45ec51ca8e7ae2d51ba48f9b0a081ee650a5c77621fdbc017e0235eebb363666e0178e8cd4e4cb9dad84710de4c5"
                            }
                        ]
                    },
                    "id": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 38120996,
                                "from": "*",
                                "hashValue": "b21d31dc22c85140dccbce0252289e45522b60d963cb5368e81c0638a6cb4aa6ccd23a18d2bcb1e1d8099fabc71920d12ae273f56cc56b0614ee6a7e44061757"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5247983,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "d8bf8b547a8f90adcb0f242b9a6748e268ff41e7462d022a0b519b356e585426e076dd3a1590591b4425f43f6a42d705e619038663e66cb44b09ab0e26030d3a"
                            },
                            {
                                "filesize": 4815551,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "845aa19b3315ed0f05f98856fee03e675659696f0f9ce793d759f45e1aad431a6813701baf63f603d6850a5032eb91219d5e33fea95e1fc23eabc5478e37d03d"
                            },
                            {
                                "filesize": 5295047,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "36524b4ab834d7c494e80a843ed3784c65ed8bd2b6c5870a5fd7abb453faf955a627653ad55a29781261fd354e4c2ac8fe6b60e803366590cda37d2dddd5c258"
                            }
                        ]
                    },
                    "is": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 38028736,
                                "from": "*",
                                "hashValue": "5c3dedd998de5091226ae8781657ff66d56a262d2e2307545fb0ed749ac5ec243b5425bdd4270c10f67d1efac46d01b03946b899d47f8d80612f824837e39bee"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5247967,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "b47183fe4674b5ae0c650659b1471cd667cebd03ff6388f329edcfad18377f40108695c666c07306b9c4236e3aba54d63decb168f939e4fc3535794cfd0f9831"
                            },
                            {
                                "filesize": 4815535,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "1f443275cb1e0d3c4aa9aff4ee062df6216e1985e830309028f98900da66fc86f11277c531a99d2ad0b6e0c6596b6ca1625d7cdf4fd43e026e1f04035a794c31"
                            },
                            {
                                "filesize": 5295027,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "ff66e7c4d2c26b2a752ef4abe5fbc0ecbe799fa1918c5d9ca3f91f6548731382e7eb8e125021ca69c56da646ac79d8aabc34dc6fbd7c67158b85701a484e9df1"
                            }
                        ]
                    },
                    "it": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 37955380,
                                "from": "*",
                                "hashValue": "e289a93554b56479415e84932c1358dd5e3358c602ec69d544d6ddf22cc513b4553c0c411b2b53398f5ec774f9ef3702f163cc8ba664ae0859c856ff4026ee76"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5247903,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "eab04b7062d3304d03853ac228298509c7facb32d638fa738821e25c9a61c235637ad75ce58df74aa4dc6bfbd635e948aad45da5a761e7c132c1623ce95bd61f"
                            },
                            {
                                "filesize": 4815475,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "004e3924bc847e83b01797a8132fc9f3ad0491ff48ab9b432866451f912c9d52097e885afb121cd3cad42fbd421684878c3d0f3c8d7f7b26d78c1754b7770818"
                            },
                            {
                                "filesize": 5294971,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "07ce4bb5737625e98b7d0af7438ef886825ac6699be1648921bd6494cebe875e46f492424a4f3b5a5bbea5164d225a9b01df292e4696ff0503811dbca494666a"
                            }
                        ]
                    },
                    "ja": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 38220826,
                                "from": "*",
                                "hashValue": "cd0b1e4fc5a8af5dc379d0d4498ecbacf8900de93f090214775f0c30294490d1b853700073bd4e3c437ec370efee7dd6012f29a734e39dd1483f426851a718ed"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5295067,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "98014ce973d48e2593e793d4903ee328d35c1857a5de66ab67d3c2eb17ad3c9aacd163a91cbc94778693e11e2570e5214764d96c93abe95630a3424f0cf361dd"
                            },
                            {
                                "filesize": 4815583,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "783692c4dc34f7e0edfb37ef4e9b0629465cafd1912d5a1a04c3e78a2aabd311ab56fa1cf929f16104bafff855d8b81ed968560a498c6f79c3bfd34c3667e03b"
                            },
                            {
                                "filesize": 5248019,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "358e5062bd7cc0adadd72de86c1ea0f14786a36b7b936a058a2eff33635aac2b64bfa89628876428a4796c77be9325f80459756515466ee0e0e37deba1c51e23"
                            }
                        ]
                    },
                    "ka": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 38220596,
                                "from": "*",
                                "hashValue": "a889811adfefeb8af9b362b0c30149ad63d00f137a73b104c00ba48edb42ec970af53a10b6d29a2c77f19da569a7ac3a5fa69b930123e278e747c1a1e615f270"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5295103,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "ab6b16f6cd295fe46dc70dbee0359b216a4ef5f34719fb9d80e8dde8ce544ff1d96dbf40740c98c425a6770ea908a5eb24ffffc5fb09b675d3b4fc5054351253"
                            },
                            {
                                "filesize": 4815619,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "8f7e08359a8d622f5a308e25218fcec6261c0d034ad928d0422421d768439b3783c37066933ce04b4fa53f05074c2ed10b0fe9023b6cb4e94be7ebd53a09d6a0"
                            },
                            {
                                "filesize": 5248039,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "0f5a76b9f65ac529e002166181c727b6466939a629ffa4813d89f1112b88431b475d17674b22049c329fecb6e157fdda971a4fc21e9b1f384e809dade4b71a0d"
                            }
                        ]
                    },
                    "kab": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 38034884,
                                "from": "*",
                                "hashValue": "0fb4bdc8fb6732e87efe96e344ebcbb378dca7fd0be9daee82eadc0f47042c33daf2c36d95e353001a7f48cb65c0b5cbfe38cb43c3928446a87031a58ea004ce"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5295027,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "540d7cdb7793b4901f78378cb5ed7668ff61f7bb98eb817d03b460c1e43f50b74d141ea35d555441cf58f8430b9ba6ebe1dc2f81e6f50d76add8119692959bee"
                            },
                            {
                                "filesize": 4815523,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "7268180867ac11e7693595cbc3e9645a6a95fa18aaa34e0d9169da2fd734208c34061c5c72f440c2f92740267198ae397b4fc7e40708f79aba812c96fbe65eb2"
                            },
                            {
                                "filesize": 5247951,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "a55bcc1500891ab1d70ce3ae67fc01cbf78e8baabbad99e2ff505c620b683017818610a2b75f9876902162ae0a272877571dd71a85efd73816c70710d6be73b9"
                            }
                        ]
                    },
                    "kk": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 38044096,
                                "from": "*",
                                "hashValue": "9a4baf8443fe58853bfc70d618f0800f5f58a43b7c12c176b8f3c64442cf62a8688abfbe8231afbcac3ed333d394e7aa90c5a5d511ec4feb13ac6ea944abfab0"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5295063,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "9714933fdd5038e6062f42d6e62f0dd78cf68b4e1da465f362bfc4f04c85120fabce9e2b00285d1ad21c95bca8bbc27f75b13886318806e2e873c3b857dc2edf"
                            },
                            {
                                "filesize": 4815579,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "e6842a215c81438d904a9307495077d273e2289016da4f7e1f472e57e815a1d4b439d31b4c19a63161766fbaca5b105a5b2f403b77819db4263f980c9290091a"
                            },
                            {
                                "filesize": 5248007,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "096c20c6c39d7d2b260176d67ed6133ebb1f7a3d4c487887333f1ecf6bc014e532cb73cc5a0e105846625277a5bea763dab9a56104d68daf562309d644ecbe5e"
                            }
                        ]
                    },
                    "km": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 38232778,
                                "from": "*",
                                "hashValue": "c36018fdeb013169d40a8fc7dfb43843e4328b78f601ac1394f12245b1af542d8def4c8765ff273810e90395d3d85186cbe7d604dc90660e6ac2d52216693405"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5295131,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "9dce7d871dac3e78a190f00add5a919e77a1955643144a9997472658bd05fdf8337534cef207da8e75bb2b5acbfe89f420e962642ce3595e75ed83e72b160f20"
                            },
                            {
                                "filesize": 4815651,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "df9b552af76f7df7752612df54050e7a6d93569d850b68f384c8a4797793495898ec1b973181a163af4177a538a18a780069c61ff5135561f3114b8967f8713a"
                            },
                            {
                                "filesize": 5248083,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "7a73ea9def67821426b76432d257b23c38bc684dcf81383e498d0787c461f11755a9a5f10c2df2eb8be929015896fca2c34130907fbbb5c39e67d3344f500d14"
                            }
                        ]
                    },
                    "kn": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 38054856,
                                "from": "*",
                                "hashValue": "4a4fc06a6462566231181d686dc45a40cbe743c184507a2b9aa3ff12c6bdd5690a58cb66a247e1b1c1ccb12a5e77433f109212f9421389dd9b88cb61a80e1b56"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5295099,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "b7dd9603ab11ddae1aeceda312242eea43820c099b7ece6b512a4976c81b17bfc06748b9ccd1ba0c95af7cb3eff8c9d433080745c3a4ecc3970f743d60bf9c9f"
                            },
                            {
                                "filesize": 4815591,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "97d15ad65c5d7c38dda357ec2ffdcbecdb9cf1d98a83d26e7328660dc97bf2c110a88807b2c729271227a93a80b028ec40ad993dd8cbe4cee4c56eee1e5a1b7e"
                            },
                            {
                                "filesize": 5248019,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "713ec583334f2673cc64046efecb9d74783f41634058164ec65ccf53a16b43c2ecaf0eca3c1e3607b1d4a280cc6ae7bae2b6e40d3fc62d3f1258115feae3db07"
                            }
                        ]
                    },
                    "ko": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 38030292,
                                "from": "*",
                                "hashValue": "428c5924ef1b322de7216f0e069a7f0fb6339e6a6efde0b8a88a955124c5066ac3463e70df4a8c4d70c66a561b1a8561f0df79dc0d282df7c3cf0aac945cad08"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5295031,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "ea5b6ecd1205d2e3e9d59f3c0cf5d296d99b654c83dd83e080d8d2ed15a89535157e32724b42ddc77e6c2f2729fccf3de3000091fcc7e1bd9c539e1afa89a1f7"
                            },
                            {
                                "filesize": 4815543,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "0167148f8dcc5cb36d08d9af6879fa1af448a8fbb8298d4f02777caf9e0577ce2581159bb5886752ad5989b3e8c6e21cebe2b25905240e941d9c0382c55c467a"
                            },
                            {
                                "filesize": 5247967,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "7f5ce8dfabd9e9de3f8ff0d5b0e1012010f84906b7bca02e3a32fbd72f78186623d3d90a85aa165a3c4ba613da2c337da8e199063d1629cba8479688d103f144"
                            }
                        ]
                    },
                    "lij": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 38210050,
                                "from": "*",
                                "hashValue": "ad7d3fb4d92dfbf888562ef6a3a867758a5622104e2dfd673f1ddbbbac98738db694e8304f179f546b56f2bf29c8b24ab6bd73befc133145ded292ec80e6f8c9"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5295043,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "b54b0c0d1bfb43dae169ae05492673fc8c311147e898cf664a54f27ceaec480fca89cecdfa8ec07757c23702daf593dfb4f3ea80e05b14dc9f37684224eabca9"
                            },
                            {
                                "filesize": 4815543,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "63ace93740d77a50a7984e3c6d4d13e2ac88456c9300110beb0915b2ade0495943c762df383dfa57408693d1777d065753f6e91905d931a685dae5fb5b6fe7bb"
                            },
                            {
                                "filesize": 5247971,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "06d24aed1914f531321e607ef0956bb4112494cee0dd0f72a7cb4c3e68bc9e92aa2b80255d4b89c1fc65b0501935f04293c501c0e7535e5c18bad7eac6bc7027"
                            }
                        ]
                    },
                    "lt": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 38313512,
                                "from": "*",
                                "hashValue": "8ea8e816914e87f7e7b031a7edd4185a2f60f5ace8dcf6402e5f7cd78edc0771a6ec6b46a84aa1092e1af29892ae04117fdd68ac6dceb589677df45c721c677e"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5295055,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "1d1039889f87ac9c02ed8eefd52a655a947f760e32c0b689e59b20d90f3fc13611a87a5b92fa4dd6ea54d721011fc7d864f2c3c514ab3a9cc34283814e48ce27"
                            },
                            {
                                "filesize": 4815567,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "b6c880f47fa246ad263dd36eb6564e5c4c1790e8cf290260066a208c6ce3c3f74baa445ba42cde41cc4304635033de9a0ae0862a7fdf63a9beb8d3d92cfd2100"
                            },
                            {
                                "filesize": 5247995,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "4f5a75d621d2eaa14eddc656d20a795f98c11605e972020d4270a34731baf74fc84973d03e8d351e87ac57b0341955cb0f5a706e20850be3bfc6c06cac6a7c95"
                            }
                        ]
                    },
                    "lv": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 38311330,
                                "from": "*",
                                "hashValue": "43e50e51ce576cac4b1da99aa706133334391c8cb0e0a5a5d3210de341a96fa46b6ba7244f08ffe52f0dfd6a64b50795297bd5c00dca9efd61619a799fce3bd2"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5247995,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "d5f79032d4eb01f123b55f0ab254521e1e37ec0785f000d725f9de9ecb3c925798aab83ae226eee458e17d503aabb8079af8f58c2eeff6d5d22abd6855d639f1"
                            },
                            {
                                "filesize": 5295051,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "60ac79dfab8a12791ced1563a618fa1a3178446f4ffffd8107a11b6441d67286685d6418a1ca28cc2f9289c69880b0177b64124c1ff7dd5e4396b5bfbc3c9e98"
                            },
                            {
                                "filesize": 4815563,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "55df29bf014f0201664bf99134f71a1af975c453326ad924ff23e7de016053142666506293c59744ee44fab775b2e1511fe3b0a6a22972a4a7a098568c323ffc"
                            }
                        ]
                    },
                    "mai": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 38045852,
                                "from": "*",
                                "hashValue": "3d959e0cdecadff3c779660cc4149435121ecdaa5abcf870fc10d94d60dee5a5e9b05db322d2dd9c4df58ed445239ef9a8fb7438e64c1f7ee65f7d64df253134"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5247999,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "d6a0488d55cd5cbdff3651e53b999ef99d602bf19296854e8577b0eda61cac22ced776f3fa6e36f3ac11feabe3805cf3be61f43c9f39718ecad1d2c33da4f54c"
                            },
                            {
                                "filesize": 5295063,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "55d1b35c9f4cf21e1707c34e90868ac5338c153756b9dce81e7563bb79dfefc0b9ca7b81c64d18fcdbb76cd48bc586031d8794582916cd164443cb163d58eac7"
                            },
                            {
                                "filesize": 4815571,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "6828762858494a328f6750b8bfae3b5047b86d5707b4c4c02dd8f9261e282e9f2facec4ad7567be00c88e0810a871c350c3563a8fc6be0a3090d5512a65746d6"
                            }
                        ]
                    },
                    "mk": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 38470576,
                                "from": "*",
                                "hashValue": "f3e2698331467ab902ab2c0747e8cdbb043271cb203db7639ef6739d30c606561c0714848a1befa763eda871b39e83a74e39c6af8d8d9c711be9ceab825288c2"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5247979,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "73f5fa7cf49efb61bda6678486a08c866800be71dabd25f00f532ea34749f4f608256efbe5cf7ea966fb4e91263d344710633812b7442b536576fc924d81bee5"
                            },
                            {
                                "filesize": 5295063,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "6e28910c53158b506d4931733d6c8c1ac85792aba92808d89e6a0f386759afb5e139a175f99888b34d8c003d836f5860e33e1baea8789b880a16b8ecd1491e3a"
                            },
                            {
                                "filesize": 4815555,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "6e414e144db0d062648394e58755b50ee2f161733ff28c0c54e2196dd887d55bfe2abbaf1edd289f8fb49a71fb41041c674aeb9c8d3c79ba410f650e360c3274"
                            }
                        ]
                    },
                    "ml": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 38052912,
                                "from": "*",
                                "hashValue": "d20ed21270c29b7878cda21b33ed9f9fa3444b97972415cc535bb17a2abc74566d497ca03855c6dd8908432cea95d970fb06e258e98ce5e6011e2b3b5f5f6060"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5248035,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "6dc239be9c2a891278e204f78b77f26139b9fabedf0051daea6f1c6f36cf6cd61269d76f342aaa841fc46dd5e4961bd5f9bb846927ba3913504ad0cdd419bac5"
                            },
                            {
                                "filesize": 5295103,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "1110bc6714a5b275eb62d8e34e789d7603785754473870afa39b2e2c42b83915d3c82c568efa38cef6c7c05b347d48e3f8d4bdd2a72d79c457d5bd2c50931c80"
                            },
                            {
                                "filesize": 4815607,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "7489f9015df74af08661a8ad4a6c0ca43f9a1278f567c10a3e245855d453ea8d9488b1a959a962150c011e65d2a8b68680d857cfe5d8b8badbe1de6fd7a2bfa1"
                            }
                        ]
                    },
                    "mr": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 38049476,
                                "from": "*",
                                "hashValue": "56242b5cc8f74c4daa6eef16752a8c146258b84f40d05cda359c85e2a73fc7e9b5255f4b660a9e3d61a1803fcf830dea16b2dbb3d4c743726eca9256ebf0d5f4"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5248031,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "3db8ccce870354ef95ca3309ce694841be1b855ca2cf2b3f7fde0f6587eeb58aab815b445df97d28d4fa99be6843c21a910b98bab1bbe2870fc000578a0adc5c"
                            },
                            {
                                "filesize": 5295087,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "49ab4a4e448ef708757265d9f465661ffb6f563ea4205a65fb8e1385fac79ec8308a52d883ab0c3a4cec0c51a2dbf53ea2bb9ce6eb58e38489621120ab2a6fa9"
                            },
                            {
                                "filesize": 4815599,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "da2efbbf40bfb2ef856abe29a7ea45825548cc1f0c2d2a55b5b4ee4e6c8a86ab1399b36e24dab37b0fedf088ec8dfede51ca1de7c662926ee5b14e98eb0ed692"
                            }
                        ]
                    },
                    "ms": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 38029448,
                                "from": "*",
                                "hashValue": "681279eb19380ba55df9674c3756463d1f3fdb8973fc5f4a3d8232d1ae87e7a2060c4253b69749563e82f0db071a70af640576298b26ff48ff50a0c9c7699fb9"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5247983,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "88d1316cb0afed7deec295c79453b7cc24e8a59e7c8779251f0a96d1070434f4d23a4c1619a95f6f09bde5db259899eb7d99891327ea5ba04f3d7a04c246b312"
                            },
                            {
                                "filesize": 5295027,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "4c705fc3ef912621489e1981a2d7db7d34ddba4ada6843044940a12f628655399f7a1f83e590853273923cf82508b606b0b8a5cbded0427c2d250f80fcefd285"
                            },
                            {
                                "filesize": 4815547,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "c3ffb873e4f6ffcc962e5ce620f8e493be80760af882624092b25efe55465fcd0cf462fe8a368e676f850bf45b3b8603abc988c4408ee37cfdedfb6cebfb860e"
                            }
                        ]
                    },
                    "my": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 38053824,
                                "from": "*",
                                "hashValue": "933cb5ea1b51882723119b0c209e1bf88a27bd5cd816bebae16286be9d0c5481f1104cb231c686a0d5e90c31bea960282957fdf1932fe615228bb3c720d27cc5"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5248011,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "e63f7f6a88701fabf6b9388dd84bed3ff5be59a7ff25124d327cb13b8a613a204261f90337393e9a4eae7e811bbd89012074de3b5870933a5fbe32c48e489c5f"
                            },
                            {
                                "filesize": 5295091,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "69f7f88ee9e08bb79284b300a7dcc99fd643d111de7fa65dd848dec11166fe27d4ca6f2441923e58cafd0aab9c08e102f19985c6057a69fe8b94eb4177436cda"
                            },
                            {
                                "filesize": 4815583,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "19f0bf61e2e619e191c3a7c04fced0aff49cdd3474b586c00e7195fdfb89496d937c7560aa0944650d6f436263e9fb96cbabdc5c13946c6543f69987f28203fc"
                            }
                        ]
                    },
                    "nb-NO": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 38027356,
                                "from": "*",
                                "hashValue": "3f7cc769dfb04d0e4d3b94229fff18a66a1614c0ff014ed9a4c4cbfe4a117391657142f25a166e7bae71ffeff8da1af41ec642034553bb244cfe8f218edd5502"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5247939,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "bbb0d0b30584caa483543b5b90ee40b6671522b836a82944bdbec7ade23aefd0be53a3f3cba21649b57e767e57a09abe3832e567a05bf0ecfc618ff2570f3f29"
                            },
                            {
                                "filesize": 5295027,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "4de7704df30a8fd43f7abf8cfb1046fcce8a4eff58b7cb018b196e2f885680b748a66d71b89e13a90b4d13d8390b7c917981bcf1eb17f0e2bd134760259dee1b"
                            },
                            {
                                "filesize": 4815515,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "ed6aa427701e1dbadeabc241922e8e78eebbd9f44a988d752ef5043d0e26c524c6865efda8f707028772de9847fa8a524b315a61c9faccdfbd3b90fa999c66a3"
                            }
                        ]
                    },
                    "nl": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 38702596,
                                "from": "*",
                                "hashValue": "ed003307476a877f4a342a5d25157e4e86e22c428866ff275bde6f223b259e9a8245fa81191088c50d521dd4d3bc198a2aca32a0fc4e2ce0699c39873aa4c5f8"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5247987,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "26bb0b9ce2e7276d92625c460135f1e4e5ee0dfbe06f37ee3a119c624df3443f954b8fd5cb349ca26e798c91f95e72a6e08d463f3f15059f36604f56bd85ff4c"
                            },
                            {
                                "filesize": 5295059,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "7764cafe6b98b4f7d2e1ddfbb2fea9b3e1bdd85378aba22ea70082e531d698e61bbfae5fb97b6ff311a203ab12113df7bfc81f2e55727e8e261094b362d784a8"
                            },
                            {
                                "filesize": 4815559,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "62024fb868b6659d497b4af4c9e09a2ec57da9a50dbf041e4d42682c4d428fd0687adfe00f2a22dfce8a40a7bd378baef0ec851d19fc7792c28c5a1628f56d7b"
                            }
                        ]
                    },
                    "nn-NO": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 38027696,
                                "from": "*",
                                "hashValue": "aececc7ff6f2f2c253ee8811d049b058d9881da9584a0c167e1f64c648db5c54ad13a6383f6d53a966007b74c95b381cbf28d95b29d6140ae2da24044fef74c7"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5295027,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "c8c507d20ad3c8322cb1e6eee54abc6144ffc10f7b9f926e2c77498f6fdedae2780187a5551361dd2dc2933d727b869ff284bc1b77a886c15fe577c9df308074"
                            },
                            {
                                "filesize": 4815519,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "877a99923efd36dd8d02ac457dcc3b9d106c1d0a1c6e5f97b7afe2e4f0f1bceea8371e2afe898bba3e085ff02b5d8cd678ea3f410e3aea596dca18ac5ab90f94"
                            },
                            {
                                "filesize": 5247947,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "bcf36e3c2aa16e9a12b2c52378ea98b0777777bd02b11caab5a33cb77fe01c9308f0e1d63c473ea74585ff65c3e1333ac236b77dbc985c36ddce63452ac0d22e"
                            }
                        ]
                    },
                    "or": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 38214478,
                                "from": "*",
                                "hashValue": "dd39914e62d110129c83a66565827d4986419409e3dd4048059af6c9529ea69c2780e81905ec41e7f77290f83dba83bbc73fa9ff70e2b9343a91acf36f40a84a"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5295095,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "a649911d229b5dfc02f3cceedf240d3b50e67b3d5c218cf5510caa2eb9b474ad01dd99d1eba967ccc9ecbc72e382964e0885cd1dfb01dd4568e5d8ba0040e19b"
                            },
                            {
                                "filesize": 4815591,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "19c3927a1bbb69d6bbb55cceb16d416afa7dc51ba93090fb02dd1a884017a4212188c9a482b685f82873c69ebe6c559b1dbbc8cfd8e5549a61c5c633204c7e34"
                            },
                            {
                                "filesize": 5248027,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "80dbcf04398d129debbfcba800adb6b3abe68780add8c1d94653db94533d99f357ee07a0b8bdc993bb6ff7772a491acc7937e1382d48be73259b056f00f1dfdc"
                            }
                        ]
                    },
                    "pa-IN": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 38037632,
                                "from": "*",
                                "hashValue": "d2209cc4cc44fba99d3b563a453734aadf8dab54e4e48c4fc4f3d317c939fe1b092f1ca8226c1e3261a0b34569d2ac258cc4b28be61fa684dd68015919bfab31"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5295063,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "51faf42f347962b6d14a2515b77ff7e92380b80dc2e53f45cab6d1eeb84100bc220292145904fd97ceb402d6a26874a7df5f84faf90e004c3382491138942394"
                            },
                            {
                                "filesize": 4815559,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "ccbcccbd145ab0a204a744601420e113c05a0167a1bae7d935b87f5ebef4b9aa813c44cbffa938f0044bb906d0535680ae98c29f9f992550fec7cbb3ccfe9e27"
                            },
                            {
                                "filesize": 5247987,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "975e476055969fada091ea4fb3c6a16bd37c864097e35dc01333fe707b9e4c81aad9ca86151f0aff76af1df349bdad337fd73b9709e880912d387f55342a8801"
                            }
                        ]
                    },
                    "pl": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 38951384,
                                "from": "*",
                                "hashValue": "a2933746dd4a6e434348560e2b099e2bcc2fdd0d957de6fc13d95eeebb81cfb554dbb7e81a45eec85c1241fcc40ebff907061285508e20f6db84c2f092e2d79d"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5294991,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "905efc208f850294d7e9bbad16b2208867164a51ce4e2ca1211319b84855a2d9e409fcec374293f4f729cfa4a2ef039dac7a3b2c565b1ae1a22b096cd50b7710"
                            },
                            {
                                "filesize": 4815471,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "4d3b8643639bee79b9b73b75bdaa85c287a2d1726dd8e22002acc971f50fe18e14dc242a72ce2d5c7817b1ddc7519648a53ede5c24925c751e1f371211dae45a"
                            },
                            {
                                "filesize": 5247907,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "7deedc813ba707b8cab34bcfea255ccd2d33ca8f4b3f5910e4ea25da7d08c634e402e3a57ba15d00bb8f1baba2ad6c5e9459956a528b44fb7974d7b832814f35"
                            }
                        ]
                    },
                    "pt-BR": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 38180802,
                                "from": "*",
                                "hashValue": "7d6979555718caf10e4602e3d594fbc291241a3d9e0c610178d5cbf981a17a5076d7c5a32de439e4b653724f7a3a776f699472e52a866fd67af07e89dbeeaf7f"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5295047,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "aa3fc09cceaf968a9ebea99cc4346cafbd9e950f4ed05a5a4530c3725754599c9782d19e2dde6fb72f93ed5ab30afbf083de831553ab0e972e08bd86d2d7e3dd"
                            },
                            {
                                "filesize": 4815571,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "6d3850d5f5274f5d0c8b184586c5d51d99d959aed744ddb71add38ccd32d198322f6483c841619adef1393c4ecf34db908376fba54aee57b4739d9d53bfa96f0"
                            },
                            {
                                "filesize": 5248003,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "4255b995a0db69155e9e6af309fb6c4408998f8908a5e538a32614b1678546d41181cb0e45dff05b09c6eacd7cef08ad3094b96cd49fb6e8b6132cb6181c6153"
                            }
                        ]
                    },
                    "pt-PT": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 38210090,
                                "from": "*",
                                "hashValue": "869cecb79cc1c33594a2fab130a359d2e094d53bfb91a2a6cf768527f59c1cb70a59ca5126c0b39c97fb6ea2ca7edec1bb15585134768790c76fe48a069b98f5"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5295055,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "9f05d5b7755456096c69bd67a91bf64d16436c8ab24bfa11076a8a7b8adfcf04ada8af63ea7653e42ec4ed276e9e4efbcd274e03830fb72c588a548c00e84fc2"
                            },
                            {
                                "filesize": 4815535,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "e4dca82190431ddc4ed1b26adb0b010f7e765916bd27168816b732e74e5dc55b46911a08953f30b7848f6ee2165e45a3751e691f6d8a9c7831301b8963272b1c"
                            },
                            {
                                "filesize": 5247975,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "77622ebade9141c66345b2a4323689e32f88545180a3a4fcbb0d2481a04cde952cb44022844b346227822bddfaa1a90175208f8af7928628a0179963b0837c75"
                            }
                        ]
                    },
                    "rm": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 38214632,
                                "from": "*",
                                "hashValue": "3379f035b68e48f740f0139030c179d877b9d616baf2bebc9cd7c676e1c39ab85d83392e852c78d05e96f9c98389cc19acba63134566fc96ae76704ef4c38831"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5295047,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "1f0f927cc8bb255204e20efd254a333f20396af935c1a75b6fb58db73b4564b3b39015bff4d9cea058234518ba46f5d4f0c12c5826a871cf8525e6ac9e19ff71"
                            },
                            {
                                "filesize": 4815563,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "70b542553490b528cdb93cd0082965a73c0a6fba81c44a41dffd07f307a4ccbab54ed69183580ecc8302191bfa934b6a6f7d09baa2f5fde078ad0451265725d7"
                            },
                            {
                                "filesize": 5247991,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "71d698f6f7ad8f38828784a11348df73f28868783b18c05ebe0a2e731d44a41b3c8f63b8c2ddccbd37d27bb32f789956bb31262f1079217e19d0c43409730159"
                            }
                        ]
                    },
                    "ro": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 38517216,
                                "from": "*",
                                "hashValue": "1d618a904e3bf5e241e2120ca17a1a771b8cf2cae8d5ca633c594233dcafcf922a3c74857f18e2d8b8c797b63314f977423d6ed4a37bdc6a392bc0b567b9945b"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5295047,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "6284cdbdc909098698ed8bafd54ef9ec4d6be36a1ed43519c4b42d88b8457ed931fd917a7ce80ab56675ebd80047c626d5e37b33d88a110b78526729138916ea"
                            },
                            {
                                "filesize": 4815571,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "64d50ab38f7b20e20e5818794b96c1fdeeb39a0c95ddf3fd2eb5fbf6c77b3dccc1c25ea25cf1a1a6dfe393d6872159750dd8d98b493ea9dee74286e2b539e62f"
                            },
                            {
                                "filesize": 5247995,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "17cb5b960df6ae1ded3d738530a32808baee282f8bbe5679336d47dd5f197c6b1516609865fe222e73c66750f75466c72c846ca1c4dfcd2ddb22ca87ff06fe1c"
                            }
                        ]
                    },
                    "ru": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 38471448,
                                "from": "*",
                                "hashValue": "0504b791c73f1641480b40f8bf937758013cd5f899b0b886ded62767da797fcdcadaa7bf943b3e7366ee2aafb8bdd3a08c4f1c4864f50c5aac2edc95f726f4cd"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5301747,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "08fe3d72b0c49c597ade941169ce370afbf3364ab6209a220200a412134aae0088a3907c492f379b13a9efa016bcf0c9a4d6025017a41a2d180df24a1cca50bd"
                            },
                            {
                                "filesize": 4818515,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "a2fbc061a8cc54a3cc8048ab9e0c6705505dd5ee6a4e561c5f3edf2af0974d0cbe91f679b460c92669d407d5da2e908a8ff9724bf5f3c1e8cb79075ac34e846b"
                            },
                            {
                                "filesize": 5250951,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "89060892f684a3ebaac5dfe10bccf7d5f9ac7e96916eae3eeae45558b939c53b49ccc122691b3500a36bcf94c4ecdede62280cedb0b388a938d8dfe64d751948"
                            }
                        ]
                    },
                    "si": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 38040108,
                                "from": "*",
                                "hashValue": "c244703721070880805cce3831021ea25d8133f61cff5fb9ae9b58fa8fe2659d05249d56ca1ced681389e662e477335773cb8647eb97b3d4913d58430fc0c57a"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5295059,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "a9f328e7abcd2a8efcbbd3827f5e588a02dff14bf6411bd55db013ac516a28061067827884342c251c070d1fcdb51e7fd2b16fe4a4861cefcbaffa045a5f1cef"
                            },
                            {
                                "filesize": 5247967,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "e0d43d80697c6f36a111d427871f1010d7602682247dc0033733755b0a3735aaefe22afa23ed85b39790f46e4f93e8521937f34410641eceb15ca4902377aeb5"
                            },
                            {
                                "filesize": 4815539,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "7b6d71c3ee48cf4df6d115e37a6a31260cbe782ef6d6b4144a850a9b550a24ea3dff4a5b8eeeb5315e6439e26e1916929238e17c4bd5c4517b1ce77b92d87ea3"
                            }
                        ]
                    },
                    "sk": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 38724612,
                                "from": "*",
                                "hashValue": "969a52ab9bb0d70e467a51ebf67cde171a410a4e7918297c4e81b22da9abec85c0932eca76fbb78f9778f63589325b2810cb5e34c704836b2d8beff2574f3488"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5295055,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "520f2680f868378c91d5fb93cba9579e0cd9d41c32fec1ae227f9fb9b37bbac3b7e087106f318ec55494e687d135a30d63c5fd2aed8e4aace2efa781e36a1aab"
                            },
                            {
                                "filesize": 5247971,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "4eff2fde346f80ccfb59e5df544608eeb8c5463978d8280da6f9572d9f1eb654813a1572a768abbe7451b15f2ecfa0d5eac33b45b461eec33f3d0468f1af9eb6"
                            },
                            {
                                "filesize": 4815547,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "d6d33aa8959cc8f04489861513adf649d276aeed7530cb610addd9777f8dfc285e6474c43f128c7aa77db5dab7d2e161cc4a009549dcf435646ab63c0ce5666a"
                            }
                        ]
                    },
                    "sl": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 38035396,
                                "from": "*",
                                "hashValue": "16ab1616a996a783e978453faa02cc89d8a7223fc6f3e3dbd552ce23ded010920b5f8923f865cb905ad007f597189f2ada432f482c61b7130173d87de4ab7867"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5295023,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "ecf0125bff5a3ce11514e2d6edabb4387f62816fb1beabf67ed9ec4e217b29827cf8cf841925a2b03683f46ca65f66741f372a375619b36ebabc1ed6728ff96d"
                            },
                            {
                                "filesize": 5247931,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "e9942bd79e5930b23485efd9b94724a4ec2af74e482ffff0ab0c97b8765c84a17682de27bc2cb4bae286759f55731948b22f6590274709ae4b782ce11c32b0c1"
                            },
                            {
                                "filesize": 4815499,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "cf3eb0dca4cd2a49a94a38bca92e5fc3fbf73392d72e6ef7ed6d6ca521c544e205f864dc30d3567aa47604b41fcedf270bb62be559413af3ca03d67470a49c38"
                            }
                        ]
                    },
                    "son": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 38025452,
                                "from": "*",
                                "hashValue": "e06e038173380d453fe5a13759b16f4fb5fb392ebbcb3a42cf968fc63564068b4aac37d2b44a5ab6c9885d97e5cc92665b7ea5108fa7fe7f7cd113ea2bb28300"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5295023,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "d6b21b42daba665b86343d372155f737e0bc5fd46b1fb018f1ce817d5f1a0802fd100fb6673ebfbe24aad5575135a311fffa8baf1396d8d2e9882f82734e7a6e"
                            },
                            {
                                "filesize": 5247951,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "f91308a4cb5f5ba7faaa6879f440d40700e81194d835b513ecb3eb46bad13c2a3994ac4a070859eaf8537bd388e6b84b297f59e126f050fd737dc69cec3cfade"
                            },
                            {
                                "filesize": 4815531,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "98494f405785c1d945fb0baa25baa18ea83b36cdac2f08eba2427c1e34e74644c571a0ceef4fa8d4c68614d2899229e8d0f85e5b0c948309a0f41be26ae80769"
                            }
                        ]
                    },
                    "sq": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 38039288,
                                "from": "*",
                                "hashValue": "68e68972513e092a18750b58f1794db020ce0fcc3dafc4a277e78546b037b1bf89a6dad83c407c0146d398e392d65a2f946ecdf8c3ffe0f198bdfe2386139ca9"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5295031,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "9a73c1952caa0d622dd0cb35d4d609ab86356b1d8df6477ec768e2e98eee4c682c97c294844ac903cb172f983bbb77cf8703569452005e021bcb633babf0dcb9"
                            },
                            {
                                "filesize": 5247959,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "db5b57fca5000bb2b7d97ce5bc48781f31043f79725b2bee33f09452184b9a759e04a7b6bae94f30e6b7523e5ae77a4a2a78f67a03d5e27d9eecd24fd56de8c6"
                            },
                            {
                                "filesize": 4815527,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "0be6e2ce0032bbc5220940d4428c70938732d5f6702efcaba472ec2f9b08651096d31279a9cecb84e4e7c1efd50bf09bed46d46a0c6ec194e56d19b735f9f1be"
                            }
                        ]
                    },
                    "sr": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 39161876,
                                "from": "*",
                                "hashValue": "a3c62130893fda17085beadd58e9fcca3f7bee21b5a7eeaa0d5b3c3bde48c78ae10f72bafaf651e8579107638eeae28c8afa33d81aa46cf0d9e26828bbe4f1f1"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5295075,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "ef192408b51296217922b48b56870e186572b773b9e3367e943522c680e187d7d7265240b8bdff053f981f7f3d3aff7917d44f067bd4ee99a18fe878d816fcfd"
                            },
                            {
                                "filesize": 5248011,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "6c2d7bacd5bc9791f118419065f4d0bade6590edb4f5cd5b5f04f5971ad3b554f30d45166c13b0f47fa6e0566f246fc7988f5d95b8fe1fdf5c2ade3a40b3adfd"
                            },
                            {
                                "filesize": 4815587,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "81e6eab596ce1d84d06d433eba066398c57e59168429ff0db3ac4832a3a10696b2da56a4ba2ecca72c3d7d402bbbff7df46a435a6e3f17791770f39ddb89e649"
                            }
                        ]
                    },
                    "sv-SE": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 38571780,
                                "from": "*",
                                "hashValue": "974a12407d600c7d929cb113bffe4a4f75d3274ab1ff3ce5e2a93d7f6250243cf433e0e85b1e6465791ca8c3966c5d3839e5631add52d480a3f71f50a9e63f26"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5295047,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "3b397fa12afbe8210c4d1727efee7759c83b4e1e9d0be70c83225571f0946c6c756d7d3d42e7a67cb2139ef40bc239341e49306583fe4e5adec9e0718b8d9d78"
                            },
                            {
                                "filesize": 5247987,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "1082ec7b9adf8a73d9a15e0be7de2c902fe0eade7bdbd44cd8155ecef59255ec2fe939d1cf283c398bd6b02d4651368ca5a99f262268ad192a88ad910901fe49"
                            },
                            {
                                "filesize": 4815551,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "6fefbaa9d21cdd79396211aac11e9687d1aca8b21ae9a47551f7434313c4b2d161abc4432c40ee08b0ec1b0c198e02d059efd60c5623f9d0e935d4accff87990"
                            }
                        ]
                    },
                    "ta": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 38247206,
                                "from": "*",
                                "hashValue": "55ee9e3f509e53f79428d6c268166639b56a73fed3159629328645b7ce5500df4cbf5dd9f0b8dd5ee2e0800a64f781fd1c08c6e1db5a8af4b683da03cf760d81"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5295115,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "e6682ecb0abf2af62a6430045d4095bfd9c3ccde2ba1016c85fa22aa62b420105d7a01ffee4878b092da1a59339e4fc25a4ba4c1421965ee0522ba2af8671d3c"
                            },
                            {
                                "filesize": 5248047,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "8d80725adf81ab7fc4ae68568461066b38457328fbf5f7b5310a3ba688ab8191d2f582952288bda2184651349a249f1e7377e34654a9a68734bd445bfb317d48"
                            },
                            {
                                "filesize": 4815611,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "8eea33a2bcc8562cb86bbdb75df9962a8b3445ae794d73a2d4b3936d7ac968b074e1789ff828da05daa18cd8e88b17c18e7c128c9eb58a24153d12598b7809fb"
                            }
                        ]
                    },
                    "te": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 38054804,
                                "from": "*",
                                "hashValue": "e41f46b32f56ce791d08bef8d78ee6e5f83ef1a06bf98645de98426e6dfc98ef0b65661aa5686d3074435dc393a8e71b51dc540661f7bbb9068b34d51fc4f6c6"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5295091,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "92852bd2a24c50af33a7bcf4d475d259ea41c1147436eae9012cdff11db6f44c96cf6b9629383b7bc4844044d08ec8fc40841176c54eeff36669aecdcceb40db"
                            },
                            {
                                "filesize": 5248027,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "90d17a3371b4a0c467e932f4b07f691d9dc875aa476b23f3d9c14c0e96832957a124d7898a1a111456662078c55012caaead87b010b8b7e58c7fe7b8cd5856e9"
                            },
                            {
                                "filesize": 4815595,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "b50ea81b0a7b3bd71506306cab8203cc9682a6c025f3ca802b0dd9582c1815c10051cd73cefeb33a97043ee28ae4184f31a4588ab45ace749a99da38e1db03b4"
                            }
                        ]
                    },
                    "th": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 38034544,
                                "from": "*",
                                "hashValue": "45ba87a40be558c344a677c33d89656d047684e45852651bd3a10682de66ee08ec904d1b87fe396386696c175719520a00047cd13e74ddd16fa84f413a722b30"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5247995,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "9de46bb930dfae3beedbd5ff3307c9ba0922f3c62456a0a146af6c0696ae9f2e6dade5a4f3e35872f386217a7a70deb7bf8603f7c1b2da76304acec22aa0b9d3"
                            },
                            {
                                "filesize": 5295071,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "87decf47fc65885bf3736eefe4920d3d05d0cd4a38758b9810bb8eead6db0c69f6a9f24f4fbfef576ed2b8ea925ab6613b61f2384d4e945c21f96c300bb284d3"
                            },
                            {
                                "filesize": 4815567,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "3dec73bd1b6bd21981cf26cbb8eab79b3a3771fdeb253bd91379a7f91e0997a68669de0106b4cc94cc913ada01ab947f144d6ec00d0a85d8cc90c82f7635ff1d"
                            }
                        ]
                    },
                    "tr": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 38033160,
                                "from": "*",
                                "hashValue": "e9de74a853ba572b46c61d0a5e23f4f3ebe4cbc1a53b3353ff3fe24ef7835657503f2baf21566435393c725360bdc1ea888fa4bfa2cb6ee60cfc42d538ac1409"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5247935,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "41d9e8edb49f93875a9ae737c6cfaf6826a1734e155f24975da7e937db5126f9caabef7649837e93406e476ba50b2b87126c34a2f75b6904728a744cd268c3e5"
                            },
                            {
                                "filesize": 5295027,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "e4cfece4e14b9c9f75dbe0616047b5e673bf79021e8618d0bcaf3dfd8d97e2d6135078349ab41a168457a5230912e005436d57cb0ef36798acb08f7826c57473"
                            },
                            {
                                "filesize": 4815507,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "31568b76c4a8a2399c92944c11166eec7b1c52bbd47c2a64b96fd7bb6c39ea0f5e4f645bcc8dbc7ec44585aa743f565a4d483d4e9048838fccf544b630fcba15"
                            }
                        ]
                    },
                    "uk": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 38921568,
                                "from": "*",
                                "hashValue": "ed1df0a115ad009738006bea610e37913ad086e4ccc69eed9636e1ff65d8c36577469a79e646a0734008e6c2d4c9b6ec9aa44cb4bec0bb2a4555751a4c286cbe"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5248047,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "e59c9c279a7bf727f05dfa6fc165b3d77ea5f43701571e1e25d9858ab40108901ad481f3c3aee3176fdf02d5bac30c74898efc156a7c16082f7739178a27339b"
                            },
                            {
                                "filesize": 5295087,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "2ccfb0bf4ab7d48bc5b43de144fea0bf104d6560d7ed9c82b9ab631948d2e44c8cfab51d51254a38d84c7d8993ccea4af9abe724ec6ab5ce16a8a2233781764e"
                            },
                            {
                                "filesize": 4815611,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "d09aaf6dc0b647ce4bb8c6f9c5f95f17f9891d55af5f94a482f0e7fd8ae6422f10c0b4384ff9d1ce42a60ca21ea1a5b683b28f621896430f5801842ec3477686"
                            }
                        ]
                    },
                    "ur": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 38053196,
                                "from": "*",
                                "hashValue": "c44a980adcc65df5becbfcf8b4cf383560490355573e4fbf614e94876eb5cec32620b2db4a3360546e617a21cd2bcee9a09892c35dac6b6b2e761d18c8f18cb2"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5247975,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "d9f7ae4409efa2b269e7907c41fde93b7e050c3cfecef11bef12d78ad99aacb7c4d403ac5a0282224f8af1e2a0394c998c93ee437b9817b74c065845a15d278d"
                            },
                            {
                                "filesize": 5295055,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "e231e218b921e80a1195e576bd006fca02d4d0f2b87e4705726cc72e4de83e1cadfad611ad8a7bb7d383af5b6eafabe59eccc4159c608083a484aeb423794de0"
                            },
                            {
                                "filesize": 4815547,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "6b8ae6db2fee896e8efbcc85c1e5a6c8b3cb3d245f1b29d3ee29856e6f66401f68efaaae5543fcf89107f49e542f3a239daa8797bc8117f80b2f231c0b350238"
                            }
                        ]
                    },
                    "uz": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 38032988,
                                "from": "*",
                                "hashValue": "5c461aa7f47a0a595dcd6a90fec1b28f85f7ff884fdd5806eee723e54390c04245228cc5906ff583a8dd637f06424484c38c1876fa624457074db027ad0665b2"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5247975,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "c0340e1d297d751b799032494122a42876ce712f565323446f5dde318c981b063878b1bf933a1a8de28ce807b167e62b2cdcb8a08518c785565744b1802de02f"
                            },
                            {
                                "filesize": 5295035,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "8538be58c9d6b5ee686439a6c540776c1af253a6892b3fd45ee7b55dcb1d8ad0caa758168d98f6e273fd8c027b727265443bbaf3727577c9e27c71763c38c804"
                            },
                            {
                                "filesize": 4815543,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "ddb8bd85a8bf2d393c2a9310bc73979d8e08ba19dba706a0fb973e8771f136710802702c325d0d5dc9ab8c1853045f2fae63e58396b85c0da8f89c81a733017d"
                            }
                        ]
                    },
                    "vi": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 38048448,
                                "from": "*",
                                "hashValue": "e0e7de0d2612c69054c43eb43f4a7db0a7960232b8b709a7e7e7608825c1d6a0d75eb113dfa38c2437aa2b0b2b1be18c953da3e35c46d3a7c5359b4821fbfade"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5248011,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "ec7cf85390d17a37bc85a017bd96de82aac08506ae5fc06a5b308af4e431701b0b7d69744192bf42b592a8585f82c57fd76f0b8d76e7f0e8d1c58504e5a8bde7"
                            },
                            {
                                "filesize": 5295083,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "47894851036d31e5a8a674bcd76967b276873d3ae287567a09f3e0c1b3462d215c2652fd6876e3a945476fd3dff562e3da36e815f1447585d53d37075e3a6a62"
                            },
                            {
                                "filesize": 4815583,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "a1957bc029bb8a2c7914a96fbc77df3a3d105587b46bf6f5bd454cfe4cdb640987eb198c8ad9d5ca1c95d3dfa064329186230bd91f45c2f1a73eea39c16acd05"
                            }
                        ]
                    },
                    "xh": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 38040896,
                                "from": "*",
                                "hashValue": "c3a1fa28ffe68364eb3936330f834ca5e9f53a1477b2feffa040b1da50611a2a9ff20ed10cd2e559c3b1a2e0f8aa51da85f16c6060f480074f5d45d9dfd4d976"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5247959,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "b0c628432df6166902686fcf2459af5a1911795038bac7f0827dcacd7940b2a0f7f92c1bce62c7bfc63dd8b1aa736da96a5670922ce7d0016076a328cc1b26ec"
                            },
                            {
                                "filesize": 5295023,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "73442ccb52bd2a7a6121a25af772cb7f18307bd8bba84f1403ba07203fdc84b472da6d7c01ed03b2e65dc870c48da6d4ff4118bc744ab16d72cb7472fd70001c"
                            },
                            {
                                "filesize": 4815531,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "17159ff5cac462e1f506f5fe60191ebf264f5abd27f7d642557747b4fcf3557336b69ca8f260f0acf51c5d14b90b952132c6cb74b646657fa17d5345f358b4b7"
                            }
                        ]
                    },
                    "zh-CN": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 38030180,
                                "from": "*",
                                "hashValue": "bebe2379691fdec894d4ed4982deac3dacfe9ac384dc6e71c90096afeb36ea78c69b4b5028af2608f9fd8889ff75bb8e67e6b20980a10e1bcc81f214fd586f9e"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5247975,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "29afd50349fa8c357e972850b76946762c6af8e19ed1061e17440a53b1a2aebe1f9cfb6b7d6522af550f6fbccd2e4b79a3b2310a27daf1d66dbf242cd35c6c48"
                            },
                            {
                                "filesize": 5295027,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "5e880b33e4b4d5abef0d228c76f729f9e688c9aee352a40152583a15dc6c62035879940c87040a9ad4fcd87436d4888200396f5db8665a65836c57b5e6f68f2d"
                            },
                            {
                                "filesize": 4815543,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "43dd2498fa005c106678e27d38a753229a304fcaac01ee8cbc8f16f461d1645daeac04a547ababc3a4d9b598f2a67b9c621579ab12be33b99bc32ceed437d2de"
                            }
                        ]
                    },
                    "zh-TW": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 38204214,
                                "from": "*",
                                "hashValue": "75c77f365c5678cf387769e1d18f716e89f0f5d9519bb251f6dc4771c832260ad195f3ee0e5db4501f377b42cfd91618434910f9280ae7d91f1cb461c70c4ef7"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5248395,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "f912e5087846d777b782eaa9c0e85f6c5546100c83f7c601a2999077a1ef9c0624aef03af5330ed86698395ec783170718c3e4ab0cf8a5bfd1505f24e0850db2"
                            },
                            {
                                "filesize": 5299283,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "91ab1f84c4fbe3c4fdc2b9ece4d9e69616040434faaec6cafab8339d0bb7adaf8de63ff3837c4fa88ec1e9295e8bf0485ff5d7500e304723caf90c4f34fd1be9"
                            },
                            {
                                "filesize": 4815963,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "5a91806ae95c5e7073d491bb696a677b1b8d518b0ea4e0eade508d2c54f072cdea8967af56c99eea15ec1a90cf896b7d4387532528336ce4d5d1ed00bde80c4d"
                            }
                        ]
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
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 41115877,
                                "from": "*",
                                "hashValue": "a157d106a7f54e1729e7bdc635d6cb1d65a89999d8f0963cbea863277b793349be208be2315f2c5a6a64c726edf897b8a779cc13baf19a9c90f3d100b1faa9c7"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5602394,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "2726f2d59ecdeb8bbdbc4e19d0d82ae989d447a9af6a7a42b1528b4f8f9ed87be16ed3e7a783106973ec72114c15cceccfe7a71973d58ae4233b78e96a76990f"
                            },
                            {
                                "filesize": 5633370,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "5794412d2f40dd2ff068bff7161bf264f4b74cab1011dc145572892f5b93dc15c617f39736dcfd3025741d96a5fd1a045894fd1f75fe1fd1bc1717cde6f5a82c"
                            },
                            {
                                "filesize": 5542518,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "6294081de6845f5adb78977f1eb47bf9c2bf88d772909f2947e721e779d1bdbb770ac111456d3511123a01b0b90f569e045b62541c17fb5662d568757162bc75"
                            }
                        ]
                    },
                    "af": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 41114793,
                                "from": "*",
                                "hashValue": "16b6ac60491fb5141ba3ada5e67bc2ae9f38933364481b4519b6345d2b1a6bbf78b52f29361fa7083a7a441a6d182306ec6d2db31430877e37b958465e34961c"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5602394,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "b5530eeb02381c9dbc3515fedb018e23d76573ef29f6eae606e32b07e76958c095c4c3b7e7ce7e1263455dee98c77afa8152b721c83ce21f431e675f36acb527"
                            },
                            {
                                "filesize": 5633370,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "f7f54d554a98a95a79a648ccc31719a34cbce02d17f3134ad8e0c725140a09ed5b893a9aab96d034ed2221d396630f6fdac04512a7f09dd492a61295c03ce310"
                            },
                            {
                                "filesize": 5542518,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "bb9f65d19967c0b1b4848593ad239e914a802a2138ae0069b04bf6219002e1a148567f55c59b0791d25095ded051fcda8713823288182514574ffe9014eb0fe5"
                            }
                        ]
                    },
                    "an": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 41128561,
                                "from": "*",
                                "hashValue": "97896197584f4953cbc049c71b0b9314a89aced996650d19f8eefb3656c661b842a0cce037898e767cdc91c3fd01139c23052131f943ef7007afd5451ccad148"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5602402,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "25ddbe3a0b53afa9d79b2f4049b0d685370233de210f7d9118d771db7ab205669c0b980d328e0e3659d55b91d6c47e659d0ea00ac89f68e65929e5249a9e793b"
                            },
                            {
                                "filesize": 5633378,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "aa6b3b39491613741ff18aabdcf6faea755557414eb566da73be6d552b9fd096a5ffd3564b1b12266da71681e0dc0e8665f440bb9f284aa0f448618b6ae5b3cd"
                            },
                            {
                                "filesize": 5542526,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "f4d55c69d45ef95a241abbc37d928cf8ec535ea624c82b8f6f787f982e1322de44d5182297956b88ac4bd7862f14e2a831ab98fb9e0bddf87405c7f73345165a"
                            }
                        ]
                    },
                    "ar": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 41131961,
                                "from": "*",
                                "hashValue": "21b7988752ce47b007680f1386846e251b8fd5e368a9ec930eafb158c771614d43261dd509e17172b630b8252d1ed6685a1fe382c1a44e2737634aac4aec127e"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5602418,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "584f21abe6b9072f40c6adb1451ce431ffa6ddf5a25f235e3dc6b4abb64f5240c1416b01092ceb22594c12720231fa18e9fbf5218bf9d7033f7c81d2eff2f58d"
                            },
                            {
                                "filesize": 5633394,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "42b147a4bfdad01e6482c4a049e03e6fa5092d88ff4560e44cbf6ce869ce627a8a02123f36ea42786a3cb8c74ac035d189f7367c6bb2fef8ea4b4869449ea9b6"
                            },
                            {
                                "filesize": 5542538,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "12f767a6d31f1868c9686b63f57806676d56195a38b1a17b167c1623963c6c49f8c0ef31c1fff9f6f2cb2d5e95760b81c07906ea36bb96460bce91c88c032894"
                            }
                        ]
                    },
                    "as": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 41126693,
                                "from": "*",
                                "hashValue": "d6ad3562dc0f4aa45dc927ac5936e23ed9a1949845c89180413160b0b54fa32bf9cac0c5095262e356c5cada5dbcc07e1b6264cfa10e9ad2468081f462e7d5ba"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5602426,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "384bea2b026eb864d8ec5c63f5010374dc6dcf58f266c1f2cf5ecb8e49eb886a6075fc16e8a7a8ab73a6dc8d0e06c3d9fdb2e95fff9d63cbf7a7493275224321"
                            },
                            {
                                "filesize": 5633406,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "7fa399d2df1f753085ea58ce28e99a7bb4b8b23a3178f6cface69778811ca95017d1e20d2e4f8ee9595a88d4b878f56efec3f7be6f2bfca79f926a7b53eb663e"
                            },
                            {
                                "filesize": 5542550,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "2b9fc03411277e4ddbf876670f4f6f7ed7a9ccd0b0acdd31a5dcca5814c6dfa7fac41d40794364f0c3b0bc3fbbc5aaf139ecd4b7473cdd2cf34a2e9651fd1b00"
                            }
                        ]
                    },
                    "ast": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 41123433,
                                "from": "*",
                                "hashValue": "98c68b70d726207d76ee464a31351666a3665b79533c9f645da2c9552822dc45b05b16c32c9f085545006573e77776e5d3d181d13903f50861d69ba0a781a7bc"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5602394,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "dba234f7740b6e0be74f999affe1cb6863c39202a2b37f379351b688cdc2f8f7cd017cc328215a3748bce6676c417376d993a56d2ebdc258adfd844277493276"
                            },
                            {
                                "filesize": 5633370,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "0a8640653baa5a4eaa2b242d49bd5a9650054124cdb09948e895f76d0e5a1e114c71ad84030c398360f98dc4440ef839c0783652fc5f28aecec7333eb625b069"
                            },
                            {
                                "filesize": 5542514,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "c2d5b25fa2a095e3cd63544953d52e7f0f93614db14e07ecd7e78a58fc3f63bd05001fc131a43dd8db23b5f5de4d6353a894f5170de2fa9a794c2584ea70b720"
                            }
                        ]
                    },
                    "az": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 41124141,
                                "from": "*",
                                "hashValue": "22db11255768fcb785778436ce9f85238c8b35236274d906d522a5da5239a275936b07648c699a9429ed6a4e1e7258b224807827a3f15d86badc954128b57123"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5602410,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "9ba15b2ba1812140e3def48d7676bc0254e929b5941b0ab1b2d0b51636670cf167965a4201a5abc17235a7182702e9318e5f6a7f6aae927aba2ff6cf99df9323"
                            },
                            {
                                "filesize": 5633370,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "be698a3d0c83d9979536268b88e6000231d1057cde6252b36874eece178029124281880a6af7e4e297205a3e4a1f37ae5623fd77f5b471555ce8023c535b9aec"
                            },
                            {
                                "filesize": 5542534,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "21227171dc6accbd08d4933c16ce001333bcede5b2d814e96d34277a9b443d4a518f88709ca5d70fee007eb5223e29f1b29e33241fd8839f66a18345d4bb29eb"
                            }
                        ]
                    },
                    "be": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 41137977,
                                "from": "*",
                                "hashValue": "30d67a4a938fb63c4bfe3d6e77f63ba35c24fd766b8f45ccf8e3593fe18e319c371b52e08be47813bfa6b82052ca9c77519d37b4143478ad22160e9c58eab70e"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5602450,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "ae1f63231f66c2488e7398ad112ebbc509e937ae5e7e400e0cd3bf5cccce86d8d7e5a6567db3e7e72c0a2fef5bbd0dcd3b16d30bcf19362b8d6f020eb02a2d61"
                            },
                            {
                                "filesize": 5633410,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "313f50ad610f40dd5456d1aac22e94e426e312d95b3dc19d3b268072244d0a2a89ab4c220bb6ee56d07e67cb449264db00f206209293055750f9abaf03c4288d"
                            },
                            {
                                "filesize": 5542566,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "15c3bdd821e26da143bb86400ac2327c3bfa5c94dbb0b23777e58c387b1c81d44bccb77278d50387abda0a6ff3b7ea2c8912ce77c547870eba588623515f1c14"
                            }
                        ]
                    },
                    "bg": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 41812041,
                                "from": "*",
                                "hashValue": "7e3316d25a13cf1dab56b90e6359683b9df78dd5c6d1a9a3098da17b01685a3e07957f85ed71004a63b9584b62415e1627f87c8580d73cc4cf793debe4ce1577"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5602442,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "bfd313f88bba838fcfb23a7dffcc8b99bfb24bbc199e7b94fb21c9db4fceb2822481e8642b1aedebf7e54423d967920df6bd09b3cbda7340b4eb527900f0bb47"
                            },
                            {
                                "filesize": 5633434,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "46be8a6e999ab51b36403084a24275234f895ba78151dfe33e98b75d2e153e9cc0f6c1d25144a2323bb1d146bde2b4b396eb3c7197f9c5720ebeabeb848caae0"
                            },
                            {
                                "filesize": 5542562,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "effbfb1f903d71ecd195d650b5081737709c1ed2c44fbf2f6e8a14f39e388e7fb4dc3f548a3445e4c1bad1220c1bc40f8c63b3de2e8d0b10e6e96647b8e7df46"
                            }
                        ]
                    },
                    "bn-BD": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 41142765,
                                "from": "*",
                                "hashValue": "d7dd67af07abbc7a575afb9d19cae2c20c9fb474fae81f7576b5ef1f86216a55b9f3261ce246a29890cf1ac8c34b0d4826cc72bafa2218011a8badfc47d68ef1"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5602470,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "5b81985853517c0ed9333602cfd5b313d45a9a19dd739188c91697f3f7a3d8c6b4a19f149a61d75f93ee5f711d20de6f3b88188d4417c54ed78c2559af0f94cd"
                            },
                            {
                                "filesize": 5633442,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "a221b07de65da6652a91f1275f0b65cc993cc241431212d799ac485052a8ae41165f1dc3126d78261c7ac21aebd783eae10d471aa4b7d68122b7c040b008546f"
                            },
                            {
                                "filesize": 5542590,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "e840f2fcf486d64cf17fb6480c22e5a51fa31ab35fc1a0091fc5b375ac3ecde32fb59d25d308992f37981a5698082c1f882b33cf04e1dbb0fbbf3e758f93dcab"
                            }
                        ]
                    },
                    "bn-IN": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 41135905,
                                "from": "*",
                                "hashValue": "15ba1ba2c8d3eaebe66e212115e25b615baf2ff21e3d9d6934a7426d074306c3972d65496d3bf0e99944fc25173d1e673a24d24b613804eadd76b5e8213d1563"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5602466,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "583b2c263e668bf9b8810eee2b93dc2845786b981fd87f4b67a5303c3d81c9162d57b44ce448e1fb2c9196c02cd811e339c64c321fb422b083b8be8bf50133ab"
                            },
                            {
                                "filesize": 5542590,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "399804c7db44817a2b5a48b048125933358dcb96ae0f1cb807a350f0c90860ad7ff6f60f1176fa89f52b26d95f340f7ba45e8f5518e3cb4db0bb4a380a8e89d9"
                            },
                            {
                                "filesize": 5633426,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "3fff690d6a0f26b1fa3883ec883f1592a78277e4498c827eda967fa8277e3b29eba9c0a4db7910ae04d0ef9fe8b5c6ad0aa3353cf04e28dcdf646ad9bddf966a"
                            }
                        ]
                    },
                    "br": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 41834473,
                                "from": "*",
                                "hashValue": "962b3e5d38fc7c10fb5e86c10fd122bb4dd9c69f6d5f8914421dd4a2733705caff24ac57f6634d33b3430e60c1345b1195c1031dc734a0d8cefa5aaf81137aae"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5602438,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "ee240acca32e95315b00ff2ce5f8c834da31eb03816a4b0ac65f5b8cedc7598a33edb780c556c5e9c4d48a6112733f6e0f5d7a4fb572857b6d8abcec371b7728"
                            },
                            {
                                "filesize": 5542562,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "7b105f876df896addd3ecb77d7cdf0d8a0d31f4dba40494cb717ec54f70c9b0800f6b7ac141bce37eee6a0dc139631b12225cdb43dc705f0421d07081d2f48ee"
                            },
                            {
                                "filesize": 5633398,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "d5a0715df8f4c98bdc8eb4fd2cc807a3c2c03812d862d336b8b8e03cd087dc147208810a44d815d38bcc3bf5c437386fc73874f28474d8aca5f65716626a66e6"
                            }
                        ]
                    },
                    "bs": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 41126109,
                                "from": "*",
                                "hashValue": "d943487c2428080e1fc87ae0a116715379721ebc7b35e653496e8e8562a7d155bab664e2900fd02eced53ecb415ac9f42c4a2efb22998967b3fb13a969357bff"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5602410,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "0947ff3102df5dbf71ce7dd77bfbae2ef71079ad0f40912058a26186eb06c2a229cea3c94123d8b7977bbbd78f406af32f4d9d984e38a89a04e4be65b9c73aca"
                            },
                            {
                                "filesize": 5542538,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "a6178293d42f5c636a44dec683caf0549ff003777e9b38239a26e4698ea62701acc8c090fa15ab0d69f97a70664914d12623670fc51976b4110acdf81d90ffd3"
                            },
                            {
                                "filesize": 5633370,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "e5b3ddc9bc9fc6c98a6f5c7205dcdd73546d4ea522973acbabc7cbca0b495acfc03bb07da4d3eacb87596c9b0a93c16d9373cc9ab7a218dbda435f7670e4cb0d"
                            }
                        ]
                    },
                    "ca": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 41450641,
                                "from": "*",
                                "hashValue": "39354b98825a52611506c313fec139dc127788267c6f5eaf6fa564fedf7db2c198fa733aa63a88eb9fff97c51958e175294d3bd277fd117ce87e3fc94cb05f7d"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5602430,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "3af0467cef198e8501f6354625f27079464f62ff148d51086d3d658a604121d8a02ab040bb249888a408e0781178673b7e4d9daf25da1947f2b2d6d55161ae6d"
                            },
                            {
                                "filesize": 5542554,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "83f49c89832b0da10c926260e8e79b0c45013cec7f6421132d36b52e72879f9d0b88f76c6a319d281a31561741131707cc45de3f6bdb327d30f81a559f565393"
                            },
                            {
                                "filesize": 5633394,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "542bdfd2964502fab002b128d64edbe4b2b05009be8b2d7ff28cf1419254421ec83ffb2676cdb6b8bc3bcede9ab4271db4f6ddb2634a82a5525c489a1bfa2708"
                            }
                        ]
                    },
                    "cak": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 41130341,
                                "from": "*",
                                "hashValue": "26719a76d8bc1acc416eb5b01e35dc8597e20ff8e1de2b781d51e275c870bacfcdcb78d3aa6911ae37310f8ffdf023c5af36f84241c18332eadcd04205ba86af"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5602398,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "195fb8a73e5021e4a05306574ae7846ec1a8a724b0aa7d00d33f9b4133fbd71743410a912f849c49f661410b3372d46ba53cb6c787511d58f61c214b2a08884e"
                            },
                            {
                                "filesize": 5542526,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "9fa853119c3768fc63dda322889f33b6d7b1da5ab2336730a9c031fed5e69d646fffcdf41fe26f735cfa7b90df35843e6c910da3e5b49e85e8e158cc0cf64e28"
                            },
                            {
                                "filesize": 5633382,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "9e5fe89686da02d56489d26f30ef97d2313659215db6186d344f503f4877a08afa8b5e58b5e726de8fcb1fb68502f570eaad4cd761ed4569a19a9165336a3b8b"
                            }
                        ]
                    },
                    "cs": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 41126409,
                                "from": "*",
                                "hashValue": "ea216523cc2f1513fc21709a26a935bd0a0ab460a5b9b29e9b9369ea7f501a70120909c2bc2c682da352b4adaac0799c0b817e101841915cc8ddbda42c6fb585"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5602422,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "1aed22e03f753aeeabb9bbab291c639fc49ef822c5821924769bc6550777bcf866d86e181522a97999bb7dde5024fac78ba06aeaa7315f453a3aab96df4c459c"
                            },
                            {
                                "filesize": 5542546,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "56ec394894eae363f8ede5d9f9fb0cf0d926475ac7ff02028133af7ae241bb413fb1d3d92ba0fdb90ea99fd8d3f81c3d706e83ab29e73d1e756960556f50c611"
                            },
                            {
                                "filesize": 5633382,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "20d29ba0fcf3536b90c6fa83b46045ca4cf66b2947a227e9fb58ca0bf55dcbfb7f8ce3e1817594590745d66d3c816a41e821cbef039030d15ec4114c90c97188"
                            }
                        ]
                    },
                    "cy": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 41121913,
                                "from": "*",
                                "hashValue": "507f4510a76d13d0684adb5dd427123e8489a39e1ee0ef12ea004983a2d1ee4908ef03c361132acdc4db84dddfcb063eb2320edae77f37fa8f4b14c520fbf6b3"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5602418,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "7dc7a2171d07b0503d3112f35fbc40f0820ead6dea85ec5651056a8c2a39995bf1f245eae837fc52dd340e90847de4ac0665138cb876ee9408f6bff06aaa3a23"
                            },
                            {
                                "filesize": 5542538,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "e15dda71adb567db4087159c022d020438c3e7ff7d2a34612bc92317d8c921981d746ffbb24bf3912ae339e040f448123ae545f2bc504696cd892754a7ba6e73"
                            },
                            {
                                "filesize": 5633378,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "80b67fdaac713dddb0f0fa08d21e33f06aaef6f212ab50e6eae0bb7df1b384e9b87d5dd5d70480a52dcce38a4323239820c696c8747cee47d840e6a918b3ff4c"
                            }
                        ]
                    },
                    "da": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 41631173,
                                "from": "*",
                                "hashValue": "b5e0833d09cf6e6ac7debe9fc40ede34938b03ba7e84c1c1331338b2d3264bc976642201a676294b04ddb3c5557548c750ae885d62efaf0cba5f1d956a4720a7"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5602418,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "1622a2ab1d3b85ee16469d24c8dc205a3771e013068007acfb50b5aab8d708198f1389c6a8117335dbcd459efa0bec1cb59b5f7fef8008f9186028c7ab0563b0"
                            },
                            {
                                "filesize": 5542542,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "1dbd85341f6115998d5a5ffbeae45838f1ff51190f2e0a0d0e09c49d1841b3f799c2ebacf215b180e3b7c6c07427974a5400cd8751299f541f6c05255748d9bb"
                            },
                            {
                                "filesize": 5633390,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "6649a8789558f88c54c6f55d2446966fd80ac4921c39560e555f06a610503c3cd8c6d6860f4e817a5d0f417df2305484363f257a69bdea64e5204d6ac8f24909"
                            }
                        ]
                    },
                    "de": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 41126561,
                                "from": "*",
                                "hashValue": "9fb474260262973207996a8dd9b1a1261dbcef9200e2adbd219fb28deb788657dcbb72a60e00bc783837ca05be2e907b9e6b75deff2bf27b607118167d8128a1"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5602406,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "86d683a058053bdea12411eee94aa702efb9f7cb60a72c542be768799e021a0ae757567cc28b476a2d50c4ddeef1a9f44a31f2b7f1b00db8ebcbc7a516229a05"
                            },
                            {
                                "filesize": 5542530,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "3e69e57077dfa73501509d39f3386971f5886b67c4829402175ab32f22d59bd5beb945f6395499f2160a1850a5bd2697f96934a51048eb76f314c113bb770633"
                            },
                            {
                                "filesize": 5633382,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "769507bb8c1c8b8d6fb8624b58577a9f2d71eb6e6a547e6ec66e005ecb9d4be80d69cb6d72df0c132ee5798f7475b7cead45b9100a6f052d8c970ef09778942c"
                            }
                        ]
                    },
                    "dsb": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 41130413,
                                "from": "*",
                                "hashValue": "0db1e67e0b9bedd2992ef1ed141388e022e461c8955c183da975229f9d0ddfb2aa1a30b0f2796ea79593138603a03663efeea23224f477c577c625acd13bef59"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5602434,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "7053b30e5909c930d0a1e39ca6973bcdf97524da72986a14930159b6ad5bd16791e6874825688ded964b41fe8ba59c150174a27e33bf9b281c7f1789520f0ef4"
                            },
                            {
                                "filesize": 5542558,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "c7e8dbaf852cec9ed6586be0e01c013c0954fa8cd3eb831a46eb3c464614b2740e49e37fc715df6ab7178bc7347d3649e72de4b6dbb57ff88fabe1016b0dd02d"
                            },
                            {
                                "filesize": 5633378,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "91963cc06b4fee88180ebabfe3ae3f7f347b2ea278eb0c5e5042bdcce2ef4893fef49096f2f628dbd98b0d872877375eb4e8bc0130ddf2616a2ee13dc010ca20"
                            }
                        ]
                    },
                    "el": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 41143961,
                                "from": "*",
                                "hashValue": "99ab25b1939e218fb81f89f7ef4907df2b3dd236c4de7ed8314d5e5b6619dd618ec6ebebbc68d74ce25c5110ac56b0991a2000438c91323f39bf301c283262d1"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5633418,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "9f372295691daabed6426f03df28154389806bbacbe5cac6ae104d2a1a2efcca11b6e0d648974af6136080ea1ee2844423c8c34dc30f49af121a794463e3de45"
                            },
                            {
                                "filesize": 5602442,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "1da016665c3796992e989a3dd723e81b0c8af5cad451b2fcc20dd83bbb365ffcd145f7757fef1ac672507b8a204824a7c543b9b8c5496388cc295fd7ed6133cb"
                            },
                            {
                                "filesize": 5542566,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "7a06875ecd6ab96a09587b3a75a33ed4e4f84cca607223e87e8be4c05f0db4be1ad8f598ec5e674c8cf2b2d59f4eabd3344640106b61bed9dbbe6fdaed3af907"
                            }
                        ]
                    },
                    "en-GB": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 41104353,
                                "from": "*",
                                "hashValue": "c25a1004cf66ddccc38a043f2913091235742a5df48cc850738dffdbb468ce5c7928dcf0e8e5a2d151243bac97cd2ad045c8c8cb3716a203c16dbdbdcd6e173a"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5637042,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "bc47567a340412f8b66d23f21b82440850bcdc6fcb9fb1db1c6d7eb38000a8ef0cf1e10c1560e1fa0d4f8e4ef06c8ea31c2bfc3fe6faf453a7c507f6c7052e4d"
                            },
                            {
                                "filesize": 5602662,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "6dd59e807bf33c914bfbbfb658660b704d5c13ad1d7fcf060f83a75d1f751cfb16f0296d6e5b677f5e514478ea73d6d07fed21640d11f006b995e5c0b80a37d7"
                            },
                            {
                                "filesize": 5542790,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "e0afcccbda9652264e219b628d2a60353793ccbfc73e11291b00bc6e75a4088b9b289a2661fa2672f5f63de6d68c92bd018b4f245008c0bf19788ef94dcf97bd"
                            }
                        ]
                    },
                    "en-US": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 41268875,
                                "from": "*",
                                "hashValue": "5b9f2939a3738cbe1d678eb3e720fb351263ca1175a65e97cc1dfffd2012ff3f01200991efec147ba5bf7becb4f1a0ae024f232b695385fee2cfe8fd3a8982cc"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5542554,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "7bb2923fadb1d807927f1ff68ae99d25a8777405e2865c34d29ae6680ff23f092d6fb30ce6658ebe68c1cfa50ee9a4f551cad3b991498cac83e245beb03fe4f2"
                            },
                            {
                                "filesize": 5602426,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "e381d2688920862ea77dcbd1151520990fcf3ca61052873d922a22330bb7ff9616718d6e3aa21b1b765f3cc19c1a78f9afb5deec80b357de6eb47bfb8e699e82"
                            },
                            {
                                "filesize": 5633398,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "20c38f9a1d6c6103a730ba5b58280262fcd722b1ccfb20bf6e10053960218aa49853aa7f20632f6a108943bb894c5d6e8e6a52d498319ca02f3a8b63b725e04f"
                            }
                        ]
                    },
                    "en-ZA": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 41103125,
                                "from": "*",
                                "hashValue": "16044dc632920f99aa8d7422bef88aca6d1becce9f368a7cf8f57b82083078ae897dae3e969425ea4e16c7608961c18fbfc48708ca93d69406570b7f10f32e95"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5633366,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "55daebb1f324737ac1bdae9b27128fd94b5bf5385522cfb3ea05c46d1820bb0f0aa2526913c4c5173d56598ddc69da9bb087d5d2754b65b95a29e7a87706c6dd"
                            },
                            {
                                "filesize": 5602402,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "68fb2264b2682ad7aed6004833adad1e9238148189438840b73a14f9b39a62ade3c4f8fca4d1c3457129bcd2990874b181f90831d8dfb12f21a380d5b602ffa4"
                            },
                            {
                                "filesize": 5542526,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "64a17b02b3c060ecea5825ed6cfcdd5d120700f270ee22286e72b3d937814afd8d403c16dceed9b4f931a5ccc599fa0dd9abc2ad5eb1642c12141123128dcc0f"
                            }
                        ]
                    },
                    "eo": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 41120897,
                                "from": "*",
                                "hashValue": "1c5683b209117b81afa1de08aabade7ac0cc932cadba2d83d95b6903070ff00b63047486da170422838cd9ca834b2f63728431f877222e0ba2fd4eaf7f6f1e52"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5633378,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "208cabadebcb086aa04451d1c8941ff25b5623a10e87142049824c07bdbff6cfd2d75fdab3895b3dade9957141ee17edde29d2d9869cff2139d22bb5b5dcc6eb"
                            },
                            {
                                "filesize": 5602418,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "791b3d5f832583a880632678d79146bfc2bab23384837cf74afb3fd455491c9086d466cbbaf5c9ade2de8a9d33369b5d9592ec9883e8091a7eb905330c91a798"
                            },
                            {
                                "filesize": 5542542,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "d05f05d2d5ab871957af86c12ccdafe8ca3da2773acf42ef827683bcd9fbc573a12ba9461f05ed066fbce3017fb3274e2f1847c876b56fb49b9a95d61316f488"
                            }
                        ]
                    },
                    "es-AR": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 41125645,
                                "from": "*",
                                "hashValue": "1a29dec3de0d1ae026806f369e0944d390c4654d06bf8454a33f6631d9050fe6af4b9e07cc340bee1d5b27fa093b9035b3f671d64e79186d6ff2177194ca22e3"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5633374,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "cef66fa3c2ba527b569ab4da9c198d736d578baece76ceb8694efe854560eaa52d81844669fe876bbfdce62f1109adda5c59b9da6bac412e578481d2f858ea4b"
                            },
                            {
                                "filesize": 5602414,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "02d5fa82ba2628b026648b8477be2180f0599f367150e8e63d563cd0a8b2e77cf718facb8fff87e400bb035659205af1bb8c72be8675225eb736b3d1bd3be285"
                            },
                            {
                                "filesize": 5542542,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "1706504548c146c9e90e96bbb93f51be4bb017164549778fcc51b91f482c971e048f2603381262c613f828f294698d632d86a56fe1fdf20db8017e78b684df1c"
                            }
                        ]
                    },
                    "es-CL": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 41127553,
                                "from": "*",
                                "hashValue": "cf7e4a4fa3c0b7152212487916bef821af0c8529a13fb7d2e8c1ba4ea9e7585b1833d45b253b7c3501ebe6c53120a2a296f425783f11350d58637ab341c8746d"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5633378,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "c0c6180dbee0b031fd129fa138aa70d0536f588c8fbff42388b981173e57053fa16fcc148e64654657e376843a4d747ee3e0fea3597b7b4aa025d35215a7d5f2"
                            },
                            {
                                "filesize": 5602414,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "7046b07267071c23319e77837f33077208a557e9af9ec87b04411c41162616f06bd74721e513679f1186acab3003d19cd203498bc6d3152336df102249edfbff"
                            },
                            {
                                "filesize": 5542538,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "e7bf4cba0b77cb8b87aff49842c0ed25a1fb60eac51b00f9a82c48d65987aabbcdb09b83ac3e9fa9d1aa247e3d4377373a1acd066d6633d8e6365fb6b2c3dbea"
                            }
                        ]
                    },
                    "es-ES": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 41050145,
                                "from": "*",
                                "hashValue": "7bc7fcb01091b60893733553d48f8fe67caaa9d5f7ee63c25fdae97ffdfcdb9b326ca23cf7b8b40b1e9775cd406eaa669c77c77beac64bb5967966722f4c8c52"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5633314,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "446b4c760ef775f924089e522d1abe5431f69d92c82f6f4c66fd1d440754f99d5c00246d4b67bf140869ad7e8b8e2b318b6d36e89d7d31c762bd3134af0195a9"
                            },
                            {
                                "filesize": 5602342,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "f3788e90bc5dbf3eca26b389374f49e5672e7199663c0b8d03513492b44096fc81d35e67c587cfe0a127f3ab4370e757b2e1a067af64171d2c6fbbf93fab4718"
                            },
                            {
                                "filesize": 5542458,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "935288c13c6340cb606190be808d9e3c34ca46b94dd1e6c323b3afc778033495c33e789b1f157c57569b415a6ff197efc7bea07e49aad72fc500333f3e28b7dc"
                            }
                        ]
                    },
                    "es-MX": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 41128501,
                                "from": "*",
                                "hashValue": "54ec6eb3ddb69da7c2a51c10183088966bd9e2aa35f6e67643a499744ec559c0575ce7b08d6b57e371ad676d969465a3b5bcc9f7a638e1e38e1df67eafcc048e"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5633382,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "b593ceb32a9aab43ebacb4b5d0060179caa19950b98a2749f589a3a6570ed4c0acdfef685a28320d812e75a6c9679c9c9e054bb37ecb0ecdf4c0195863e43fdd"
                            },
                            {
                                "filesize": 5602402,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "9fc44d844acbf26b1009391cae62e94760f655144c8cfd3be97e65766c0aa38887a6fed2699c1305b0f20883f9dec08e48a724b415133462392d1132114c9ff2"
                            },
                            {
                                "filesize": 5542526,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "072947d590d597ffc628b73ee54535eac34594cdf202ab352268a177b0c4b93e8db442ce8724cabd389e6b424ea719325da085caf84f414ada639187b9f1e896"
                            }
                        ]
                    },
                    "et": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 41747057,
                                "from": "*",
                                "hashValue": "7704e95dd20691558b436f4397be7aa84d190f0f7d7365a50f762f8e38112c6dc5135196aaa84303cc94f75353c46037a7006035702390d7c331ddd55dc1713a"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5633390,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "5f62e2052cb8837400cae67bc53450d5adf5ab8d92681507667a6dfc087838c73ef9c83145ae9fab43140dca120d1b2115452d54c6aa2f060ea7524a785e7f65"
                            },
                            {
                                "filesize": 5602434,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "b62bdba888254a6f84c36db90d9d1defcc5c1e5324ff4bf62aef26f6e00f1ec1fddce34aa113e6d346380244ea7a9058c100b77b8c8ded788d9b7b265909c7b8"
                            },
                            {
                                "filesize": 5542558,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "8a18b39a8e9f2030cb2943475154d0ab01abfdb046381b257a9634911ea490958e7a722fab1beb1d8392485baad12ae37869242ca81872382c466090add5e2c7"
                            }
                        ]
                    },
                    "eu": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 41122885,
                                "from": "*",
                                "hashValue": "fb99f06d9a273bf1217e60e393edd5c67c3620d95b529970255f47e26dc79eaa60c5bc23e81353f744866c3e4e8abf9239fbb953060f22529a2d53b5562d0502"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5633374,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "4592bc944c4eb0f85f249449cf31176a812f1444b383ca6f294c43ea3c43db5acb984e8aaf85e5b79bc00a5395d6ade75fbeb67f04207bdde515c317a056c17b"
                            },
                            {
                                "filesize": 5602398,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "d0637dccfbe47c809cb30993138886d9e425ea570820b3e2571a48aa301f4055e1add836128ab1e6b0abf4073ebeb5954a28609fcc40932a81862aa9ce26fbaa"
                            },
                            {
                                "filesize": 5542522,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "64937bee4e9bb685b48b4e1d597b137ce3ac4d664ea3c19729271a449e4e0eb490b85a750d43af00355263b23ddeff71d8568435b8130abf8ef2566de0d61b86"
                            }
                        ]
                    },
                    "fa": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 41142613,
                                "from": "*",
                                "hashValue": "382a833ca440aa2b563a6551e32c2f50a96228781f07908ea6ed53b4db88cfbdf50af38aea7c9016b6c3d0103b9994a3e9183b0cb330a922abaf89fac4d0bd89"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5602446,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "d7c09a0d8d559a2f0c3405b24bce939e2f8802d030068c8277586efe2cb7e30da6eafa9697eaf6ce67b7945a8136f8fd40189baa33bc2ddc2c79589d160cf899"
                            },
                            {
                                "filesize": 5633402,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "57fed1ec0a2ae556e8c2b540eb406c3740b2b875feec8a3d6f327b7c69984702e2befed3b70c0035d47c5294308962b68ad9f037b80dd0f449c9e1ad0803c264"
                            },
                            {
                                "filesize": 5542574,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "16035ef0bf117f25e43b4a51b30cb5c0b991665fcd476b1e4ed671672c9ae50fd2c7d28ed9bb06ab3854a5523d45206ad098c33a0bf981129a324e9567b5752b"
                            }
                        ]
                    },
                    "ff": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 41123197,
                                "from": "*",
                                "hashValue": "7c670420d0301262498f93475eabf52652b22f9ce110183274842b186651177b4f871a6519ad03b02b22de36af9a8195b04fc4f8764a585912ece29451ee18db"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5602402,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "3462b1687e788f9e741b5f5a0e642e71c3cf6d74d443d7b4a133cb7c35dd80633d3306eeca757e559f3fc7f5eb0cf6d3834617837ce867e85b4c200e8ceedab0"
                            },
                            {
                                "filesize": 5633370,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "872fd4ea92b62f4851fe987c3b029dddc69cf5fe08d971b0ff913d76a39aac61c503d6bb6a652cc5b53243bc9dd16c77c5b1328699428cfe5cebb249b26377aa"
                            },
                            {
                                "filesize": 5542526,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "86443502058161c8c05191174a255dbad382c6e91c68bd4d692cebe97ef29ea0d9b5474b892c55a869f1d5e0a025d3a97c577bcb011d2ebfc33edb0e8aebd6c0"
                            }
                        ]
                    },
                    "fi": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 41118465,
                                "from": "*",
                                "hashValue": "bf554f1a5e02916f46dbef52e14a6b82fd85a397593d34d66f7f5f9e6654e54835df669feb70643f9c168a22c16c5a60d1c0ec13a275a8de1f2cfe0d7cb7c0c9"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5602390,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "e1adda88e9b06b7adb05dbe0c48d7a7d580bc60cb9f98f147e724fb9d28fa6e832ae4b2d5b83865c56b4b2ef7853971ac49478f24d9465856512f0b8e00e1d44"
                            },
                            {
                                "filesize": 5633370,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "c1677eb05b686511e5cb5725a3f3bb8cc07d0d8298a0e59192bfc8745fc992c21df9696edc3fe859012f33800b859ef52f9d8c5da895e6c629f4780d97fb80c6"
                            },
                            {
                                "filesize": 5542514,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "a1ef9cad3bfaba3607af7cee3dc3e0962e6fb5137e2e594f284d8fa3818d15774f81542165a16c35e393aea0e7528f8c62dca301bd8273b54c8d3ce8642169f3"
                            }
                        ]
                    },
                    "fr": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 41411741,
                                "from": "*",
                                "hashValue": "e92849b5b30b49bdf1c75d74c9ade347739890903cfa81cc7c1b156502497310aee34d81700126909771214b65027166e541a74abf884c18f53b4e8cfa12fa7a"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5602430,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "9ee3c8d00b71d886f6a86647531b9e92b8a373035fdaa2489a449401725ae4946c2486a42c448d7a54ec675ccb406c1fc1a6d545233fc3c9da81db838b312a32"
                            },
                            {
                                "filesize": 5633402,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "8cf9137ea41e917e097aa004fb3b8c475a540d3afd02be23efbe4a4b4404d697d3b9a6c673cf16e74e2b55030b60bf55194063299ca1d4b8edf211375b25b5f9"
                            },
                            {
                                "filesize": 5542546,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "92905cd7e631b012360c5c9a32afb5173052c3b66faea1ecf4282f25750553d72a29ef2f655654aaaa6bfd123a1ac776d46364a575cbcacf49f95728cd6b9831"
                            }
                        ]
                    },
                    "fy-NL": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 42413035,
                                "from": "*",
                                "hashValue": "6f03886dd4b014289d9893a6d73d3fe94b3ed15490643b56667912a38225ba727e8029033d7ef0d512158d7edce966955e49c4f7a52c507049baba072528a4e8"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5602426,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "6393a778834c3932de5293dc69e4e2236b33beb83354eea6b7fe8e4173dad13f14548ba183d2b82cca3290d11361dccf115779e36bb6d1d590f95ae7097409d8"
                            },
                            {
                                "filesize": 5633398,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "9978d77f64e04b79416254842cecfada4d36fca68db1437c2173b5b5a7ca8eb2bf444146683f1e30e7de99a4ce147f8dcb989afe485771a89f795da66721e517"
                            },
                            {
                                "filesize": 5542546,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "e80f2e073dc869ecc6ff21a056212ca0b5bb2712ac38234915079dd4a856d756782454acaf03e97332c0be10dabc992c037dd7b8eb37553fccf99992277dbc6d"
                            }
                        ]
                    },
                    "ga-IE": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 41130317,
                                "from": "*",
                                "hashValue": "1390f7393eee95bccb10897101bf8675e1883a55ba5bdc2c4068405018d26f824cf9a886cf4371a7797e099a09dd662df66700b5da150daac8228f9e95779421"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5602422,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "cdfe5c5b69d444448af75ee7c96763c9af10414a2538b6fb3bcf1cadf12b6ba1e7bd23a50d480ae31df0b57c218c56732d8f94aa2477fab44377030b8a0ec22d"
                            },
                            {
                                "filesize": 5633382,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "8201ccadfa8f20d6f0dcc3a97d451b44b7900ea4581ddddf4b432795d74506947bbd0e1173d57eaf46820f5a21c0cd10ad9c943f6d30f5ae8e7fde2b2b34cb4c"
                            },
                            {
                                "filesize": 5542546,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "316d0891fbe5f80bc00d343102b711c03db6b3e64fc70bb113a11844fd34581f74cf5ea31953bb01a18f8ddb7d4c54b7859da70310d1c4318ec2f27463eb61c2"
                            }
                        ]
                    },
                    "gd": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 41125169,
                                "from": "*",
                                "hashValue": "e63ffc7bf5c954d663dd9361d23dbe4ab38a278946480a1edf93cc71ec754f47a3f0f7d92deb0f182a958bb1dcb254aaec4c03c1f0062ade37c9a9d19c0e8e47"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5602426,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "4d357f64cc9bf1c26780d857c1f9af769ea7bd3d256acf7a7d2b9e442e0a5f59a2f960df6dc4dafd0f844439ab3cdbb0f4d6a4712e83116d4864399b5caad885"
                            },
                            {
                                "filesize": 5633382,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "a9df8ce09e3e704fb2852ec02beed17f851fde6ef25206d92081c38398a39c28c4c1711a9a5db7e20f436f9f4610a6f36210ef357b0d1a91334080ce3040f1f4"
                            },
                            {
                                "filesize": 5542554,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "99152b1f0969fce98d7f6556bd45185ac4bd7bfb9f4847c681abf446bec169d36c0e062928f51fa572bf43c89b5aa14a129c3b970947fb543eb3abcd35b146cb"
                            }
                        ]
                    },
                    "gl": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 41117841,
                                "from": "*",
                                "hashValue": "d3454cbe23ddbeaa21eea83e965d850229373fbfef8f900928d790de83177e987eb77941a141c3dd8f9c530872e2f20b04b5ae423556a483ccbf828c94ac26dd"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5602402,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "bc4c873069c1a26d56af6f1401a57355c79bc29be7171455607e96bdd0252fa0a6a127920b56b90e2084cd3188b36679a16e74173826450ffcbda7c9cad9fbd4"
                            },
                            {
                                "filesize": 5633374,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "b94d85c464bba5307337d438171afa3ea3e3009d92bfc97632850abaabf518c2622202fa3fe8c132a08a589d1ad060579a5ebbde091611796d21fa31fbdeafc1"
                            },
                            {
                                "filesize": 5542526,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "c34b8a3a67b1f8828ab185e0cb947d07451b8fff22547ae567d87a531f01e89f47a71b63d581bd3a3ed2c3f0c61f9cf303f8d327e7971ba61d4062ba37f396e5"
                            }
                        ]
                    },
                    "gn": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 41128557,
                                "from": "*",
                                "hashValue": "789285e1643f1a1eda2975d8a008bf1d34781732392fa7bf878e0663edf0f2613a3f5fa8fb6f3b371a4c4e213a9059471553e4457386932a1eebdf968fe5b321"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5602418,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "679d1227d2f543c847573c8440acda63be47f61cbca70f93379c27f9de1dbc2d55b187ec51f68597d7bacf04ee26306ea3bfbdb7cb29105ee7f35ff26774514d"
                            },
                            {
                                "filesize": 5633374,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "c033cd8a52ea59e626962b49b87c52de753432880824faa88bb19e78b746777b598df89aee7db4d885ba6ed3b8b7745a3a2bc6e4170876c769967dcac7521df7"
                            },
                            {
                                "filesize": 5542542,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "b9047ad8e23eee85f942a07c7ef47a8d98f53337c01ce29062d6c66dd96a9afba8237c460e018caf654f8da0760df834c57ece4a969fbb219e441a2035e273a4"
                            }
                        ]
                    },
                    "gu-IN": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 41135165,
                                "from": "*",
                                "hashValue": "d2d09dc42e7606d395a3a1986b6567b1af533fd39360e84449764f048a31759ff62a730ac8dcacd5895b06fd4d6b6f2318b312c1c22a5695a6d2be5ce9e8cfef"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5602458,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "cff012e42c81c06876d2edc6eeec336c5ee240cd99b00706e2753706711b88cdeca0421a68c4cb08326781df48f8e3d76fa65e53f2f01d3c4f96cdbc6071102b"
                            },
                            {
                                "filesize": 5633414,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "87470dbc7841a0efc7fe2d0620a49fe361d2e6e365a284117e8229f9b07f107f5ac0174a630e8c846594d8c8130d4864513ad3e702e08108993a9787a61e2201"
                            },
                            {
                                "filesize": 5542586,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "2c30852359584ef001ad216adcf845188377ffa199dd54ec8890dfac54c618fefac62de8d6d7e5c0d3df7dab56b4715b24b8169b17fa879668f6a29fee7a2f39"
                            }
                        ]
                    },
                    "he": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 41125257,
                                "from": "*",
                                "hashValue": "9cfd2923f45c69538d77202236968ec2df1e7a65ca8cc63f897235ea0b85b6d5b297046dac43113aa5f53c9c6417eda7294f888b1d4c09277bb2d8a3a4782fac"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5542538,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "c337be30868434ca0d3fdd65b5881dc2e0270241284161599adb03b20e81e271131b4e1fe2cf16128c7629b8c3d7fd0451ffacf2d3fa5636dea40d0533c56e94"
                            },
                            {
                                "filesize": 5602418,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "d16a73a9e015d2c1db388114ce22cfa7ead74f4f1b1a9ae87370733c7c0d91e4397c63d6b040889e84231cfd89a1fb4ee28ec0b0a95a62d383c4317f483ae607"
                            },
                            {
                                "filesize": 5633378,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "7e7a1bf28298e2cb26c5009c2b8736c5eabc9c51ecd7e09b0ee64f612113001631da14aa4c90f0eda85557d9ae0ddea3366d4b2dc0bfab62033af07c3a1749f0"
                            }
                        ]
                    },
                    "hi-IN": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 41142261,
                                "from": "*",
                                "hashValue": "7ea3b5152b9cc0a1dfb7296b744e115cea7f152f7cdeee62492d1b949ad3bb7a6c84d35f063684f6433314b87e5a051a520f6fb08b499319aea167ec510d18cf"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5542582,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "c33bc3d84d6c486cc226a1dd607516ac497d3f619d47e81ef4ac07469b56b7727236cd4f1464541420cac7acab89967ef9c287734e9850b80f6a7797d8237f8f"
                            },
                            {
                                "filesize": 5602458,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "2b1de798fdd11b025b3d06a4acf84b88ef3cc38984deb4023c988d5014d6b336050c2042b7cc2e06acf6a68dd071232eb0876624c41c9dbac8fd60862745c0f4"
                            },
                            {
                                "filesize": 5633430,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "1f03499f241977c423c5c4e2a0821c26247350771e6f1154458ebb392b7bb7a9985c553392dee5d04cea7f9f8d47b71ada141a4b3b817e3f6fdc5e64b42827de"
                            }
                        ]
                    },
                    "hr": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 41125353,
                                "from": "*",
                                "hashValue": "a538fcd6b34d5b0a7e8900dfc6effe68ad34431497ce4a82e05fa87dda3d5a68fdcd6ef7a32f17d38dac05de1330df901eda66978ed9f07964b057b48ead417f"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5542510,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "6ebd002f16588d51d137d97f680004d60b4dcf740a58e98da604584d56b15afed1b36d2de5b6e4d36cc557ba76a8c001990629ddfd57aa8d321cf95a31d1358b"
                            },
                            {
                                "filesize": 5602386,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "a70a0475a56e37bcb243033d9a3cfe80ac13f86df802556a3aa90eedbea71dbe0b4fa63b008f92bd083521c7c5c95db93b0c680c555d6539864aaab9b75123ac"
                            },
                            {
                                "filesize": 5633370,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "8f75c09c4bcc4e4b88c36d0abfd900db77027adc3b0a3e99ef7e9a89f9f34e1b073fef1e35bee9def6cf0a3567cbe8af29f38fa965de12aeb5502d28d00e8008"
                            }
                        ]
                    },
                    "hsb": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 41131545,
                                "from": "*",
                                "hashValue": "b4c435ee5cbb2ea1047fffe2b37af5a576428dff13ac83a7efaafa0b4ede7e2986fe3b4a2ccb474ad212172882f80b54d491600c5af61fda047e87b219b3d912"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5542530,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "d05e9f579285d559ee952936333b15f91190ce2b6d3b304ef307d18f66c0d95bd3afb685d91217b6be7d0dee5c935173c2e591a6ae615b4882e80f515a86196f"
                            },
                            {
                                "filesize": 5602406,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "81820e0cdb7d2a04d88666e32baed8c3610fdb80f8dd539820700b5e173458cad78f9cef4090ab6ad1486f5e55ba81d9485a3d5b425c75181f6bedf1be8161e8"
                            },
                            {
                                "filesize": 5633382,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "051b770d34937ed838324596a0c4f28fad833fb6cbac969d835929d0151bdf99fe60f452c8c565e7f5027d1e84c528c2dab9802ebb7273b39be17d3059a35def"
                            }
                        ]
                    },
                    "hu": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 41681513,
                                "from": "*",
                                "hashValue": "fe06950029cc98f75906fa9ed6a9d9ea3f4e0a6149bcfc34713438e4f263c96d2dae2f7cb7823c6c3ee5a3b2efad797d046733bfbb02360e4d52c32c60c2a6b4"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5542554,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "8a7995c7bcdc19da5f0e72388eeecdc2cc219c98a0274ee5c55ca85a2835ca65149237ac1cbc74325d37e988e427cc4b99b29faa7aa53f02c5141eb4c8a8a377"
                            },
                            {
                                "filesize": 5602426,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "4a64b7cbc8b1d408baae39b1ebace44232f24167e76906052a728c2c378875f77691f40e290e7ddbf331105775b0c7b2dc7396bcdded8305fab5d5bc7df366b6"
                            },
                            {
                                "filesize": 5633406,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "39f54a076398ff9bee121a4118130862eb7c28d33b8419a70d19f965e960ebb05833a78af1b4ee921babb194243fcfd3f12521ab3ba62dcb7e899ec692e702af"
                            }
                        ]
                    },
                    "hy-AM": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 41135065,
                                "from": "*",
                                "hashValue": "31693eaa9c24e0dea1b5a443f696c69f4ef2d5bc821543571d852acd0005e68d8edeb98f39e4872577ead776c5efcfdb57ab1743bc73834f22f43abaef3ca2ab"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5542546,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "d0b7d2a11870bb119b9e1e84d6445193d51af926f5b059cb506c43b770717cd0382d10783e286e21ada50d3ba8c00938376b37946ccb0281d5c5354ef413db71"
                            },
                            {
                                "filesize": 5602426,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "0997e77341e248ddb87275a716301bdcb84e1a8966821388445a7978c3e75937a7917c027a12c8b1d72ab2a4a617be74757ccc7e3b77cd8acd54b687ef82d5a0"
                            },
                            {
                                "filesize": 5633398,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "ad84b0a14f4e68241db745a2c8b048a94b52057b0e7d9092706457e248c8abb0faec07afc3ddda266a7cfb454d8a8e391d07d352081b1e2e2788e9d25f701335"
                            }
                        ]
                    },
                    "id": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 41212181,
                                "from": "*",
                                "hashValue": "929edbff015e1b64024b409cb7933fc49efef42b0f9a58ec793d02fada9c9d75d092fde0d26d1e43feb4ffbb470fb571bf909f089c4f3caf1a7083eafb2f276c"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5542546,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "e18ebffd3e7c6b194e03ddb6930f6e626a711092e4f9e8283b2a97bc3567abd525bc9f556fb6a38efb7543c11e339fed35fbed41ae90c76d30a394afa98c65fe"
                            },
                            {
                                "filesize": 5602422,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "b44acfa6910ae89116d492b5bdbad75a1696ef15eeabeb3d556f3671b610026916c04f15c71af1c40b77c9d23e59a851204777dcb3a96b47de5cf3fd5b10f945"
                            },
                            {
                                "filesize": 5633394,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "87bee34aec7ea695775848092af6948b363928c23c5b631f98f3d774a0006952d344bfa11a476f127b30da862380a69d8f586434d28494ea0b240112fa0d6d91"
                            }
                        ]
                    },
                    "is": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 41117549,
                                "from": "*",
                                "hashValue": "bfd64f86ffd534eeb624fb810f3de97e74a2ad00db713929707f987a6a8d245893749ac5ceb3a00781275ed0864e1b24d2fe5fff20515830b8c1ffa6a064440e"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5542522,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "0cd60d9215e5d9a87b0258260541a56085a120fa553cb1683854525b365bc122794f9dfc50e389b5eace69106b54d71ceaa5c028d81d09174e5757dbeaf316eb"
                            },
                            {
                                "filesize": 5602406,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "5b35cacaa984693e2e15dc987d8396c49002397bee676fedaeb9e6f864da65bbcdcec4ab5ec20c8da82e49196559ee7fbe3a2aadcb60ba6b178e03cb11d18dc3"
                            },
                            {
                                "filesize": 5633370,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "02c184ab6d85b7854e9d8bca321665c3fae346d7151d8bd1d594fd85478e4b6174ba4f048549919c8ff0e959bc71928e6cdec266c69ec429aa2ff09fee747751"
                            }
                        ]
                    },
                    "it": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 41045805,
                                "from": "*",
                                "hashValue": "0344747db0d7cb301f95d0d445879b171d157ef7bdffe62ccdb13cece450d46b7f6fff77ce3805fb1feabef6a84d2916f72eec1551da509dc44e0452bbda568b"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5542474,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "03934e1c1a2302f4fe10efc42187c4712301337e15e9ea1948c4e500f438f5633abaf0894dba140f0eb86ce9d8c18ed37ab368116bdcbe55bda681e5fb5c6d1a"
                            },
                            {
                                "filesize": 5602354,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "279fe78f08344af17b461ffef100a399dc4f94e74aa11899ceee2fa33b96efb46c9cb9911c1ef6ffe1aa5cdd9ad8758f69727a209a8740af8ca1daa9d179b104"
                            },
                            {
                                "filesize": 5633314,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "a5870cf6e27e5a5824aa7d7f8fcce630c43fbcc9cb49a8fa07008d832af980195222cebc2de5ad7ba570f233a048f5f7d4fd8ad6cd8b77755fa41d238d1f2c9f"
                            }
                        ]
                    },
                    "ja": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 41313339,
                                "from": "*",
                                "hashValue": "dae6c1a3fd19b5fcfc08b1ce703bcca09d674183935328709472d264c413066defe52093ecf7b282a89d8f0555fa4218bb7546586a3c790890f7518ca92eef87"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5542582,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "d648508923402d61abde9dc70fc0929da61b17bf7365eec0459337f55ef1d369b34c19b9b2826479577613fcbcd2f11ec55c99f36e854ba4dad782b41b538bbf"
                            },
                            {
                                "filesize": 5602466,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "e4b3c720d6ed99a663cd1616e682fb3977760aca6db89d1aff7632c4a16087c84e7c08a0dcee74acba784e60fca850ca36d68d568b7428f40e1a2ad96e305f91"
                            },
                            {
                                "filesize": 5633414,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "5b5652f47b29a45bf098c1ff2201da74f4ae831432e8116c70daa108420751677913a247cbeffaef649a1c8b7985b2ef2ae86f77d12adfff74addd96f367f6bd"
                            }
                        ]
                    },
                    "ka": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 41311085,
                                "from": "*",
                                "hashValue": "825da53e98b4de4aeb9e1f1774ba67f698e08132b485537db0ed89d9a7fefaf7754d8c628b29432b7424db149a0d511e46036996423103fe8a7a5a76f59eeeef"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5542610,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "ab4aaa04025491b2d02d578ef71b3b24265f997c91bdcf07d7460711835657d1092bd420361e144801cd141f1320bb8c3cc0650bc106ba00edd7cfaaf59c0766"
                            },
                            {
                                "filesize": 5602486,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "1f6d25696a910431e4e3ad5c0f08d6ea88917c05a35f9c34037a7e7019b400923afe5d19795bee83a25fc95f394c223d3627f6dba60c0b71935ac30607d060b8"
                            },
                            {
                                "filesize": 5633446,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "97cc7d704c83e30999558b6b9612ca2694152e02c76e827d4046b409d8a2744ba8d9526d9321b14cc735cb5c1f1ef932de27d57b235e06c6da595cf541502b63"
                            }
                        ]
                    },
                    "kab": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 41125745,
                                "from": "*",
                                "hashValue": "776f6edbdca9549dfbd6a420ab37036518a51671b1795f3b8a436f2b0493358c220671584a0334f833074f79bbcdf390c82056c14685a7a982875d0c01b5583a"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5542522,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "3578ea10181a9fe54d8ab5abcaac0d413e7c7ef60f2fa95427c23d5d709410be69d098701811aa351e234e496aed3ad789bfc636861feb35d4028fd6379388e4"
                            },
                            {
                                "filesize": 5602394,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "638b09ba5217add7d4e6618b4047bcf6bd6ed218cd59f0608c13a970e0bd1001461d5aa4a4dee7d19709295e1b2c0128ad0f74c026f2ee95fbacd1297ddb109f"
                            },
                            {
                                "filesize": 5633370,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "6292b6067b9744425c4233ada68e900beef281d66009c0219dfa8288fd4d58ac75ab86596692979aaa1ef411cc30619dc9d0a42ba24ba4268cd17fe163271245"
                            }
                        ]
                    },
                    "kk": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 41134817,
                                "from": "*",
                                "hashValue": "1b1d7dff244797ecaa4b37379c47a120987dca93bdb477478444d599a7424112f309f1e22bb8f22b1a44f46c047ebd5ef7b7910bde1a07166bd2537fbf4785da"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5542570,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "97cd6fadebbf40c733406aec4750be3478a9a0b7701eecca96f3672e39299a0678734df368d064ab5eedb04680186e1ca5a3ce1832097813afdba342e1a6e96b"
                            },
                            {
                                "filesize": 5602450,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "9b254f10231fcc1af904fbc6efbd26e06f9f70ad614a940062b67134ea04d93a9cede9b15337c2cc09eeda33f964317dbaf3b4c8914ebd33f206f432a88e5e22"
                            },
                            {
                                "filesize": 5633410,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "f466c108449f09329299a5f0cd4c9089c65e67c48b5ec1c96449a85267afd3734432e49863dd7b3af9ca320fac4178da7baf210778e44873c88935850f67d555"
                            }
                        ]
                    },
                    "km": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 41322691,
                                "from": "*",
                                "hashValue": "a492bc6cd6d4733ab0d7c1290a6eb69a9ecb361a572035e0b95e707bfe1aab140dfbafb8062513ca39f9e675fa312d5f43638a4ae7086b442697e32c577b54eb"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5542642,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "95f3ac86e71ce575cbaeca0e1a2bce0f6f1cac8350313281542fca4f841fd0e46fabc770fe2beaeb4c7a621143e0a8ea92195fbad14f6078b3517e1b68f7bc8d"
                            },
                            {
                                "filesize": 5602522,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "57d53a641bd40db492aefbc35250710a98a960582f0efdd699a84cf9154cfaef83749b77bbb8c29e4579eecdc14a613a418a8463a2d1b39c39df1488b46fca56"
                            },
                            {
                                "filesize": 5633478,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "f540f4fffa0ac8f712cccd35dae415581df8db39ae5620da1940203781e1309e4eb4b01d06bf1310624bfc4258012c7f59d9ddbbf0f539cb6895cbf64960a0ea"
                            }
                        ]
                    },
                    "kn": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 41146073,
                                "from": "*",
                                "hashValue": "a04d4b662c8f321b3cbba1bda236dad5d1fec1d24adfe6c141949f1531919344d284f175369c4c151d02636563efb34dd29e580255e6c38d86d6de155819b0a4"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5542594,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "0439a300a9ce553fe1a534ad8b95b5ce24738e1242f4fabbf7df598bafed86850da80648b9517f5ba3b0d24819588906cd3857488e0b9720bda645e58a15126a"
                            },
                            {
                                "filesize": 5602470,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "9f065d960336d69c2d62c58cb14958cb0b7938c4b33f2dfca66a87fcb9ebdaee62dbc59c9cab9c696296a7e5db99dc920fb029e880f24da63e846ab417742275"
                            },
                            {
                                "filesize": 5633446,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "3dfbfed56da13e4d98c0ff82861422fcac5bb63c6251766869836d1090791968b306c786e0cfff0ee36c6c49454d602e624771cc02faed3725bb9eb2576fc502"
                            }
                        ]
                    },
                    "ko": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 41122889,
                                "from": "*",
                                "hashValue": "3335e57434d1bcfdd17579e782d40f6787acebc3e2dd05b9aa7988032290956856dc5e9a3a8bbd64d7443f89b11a5c24786e66b38ba420d401a111158a209c54"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5542542,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "b11be3a3083469df4347b67ca6cf498de923af8d38c7c7fe7dbcb420021019d0f8cd165bb46ae64508ec4f477b9dde53f9ebc3fd39eb3d0445ffe9bf61bb81ac"
                            },
                            {
                                "filesize": 5602414,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "e51f5bc516bbda97e5842ae000133c639989bf2a9ac8e68fa3ac78da36efc9c33efb4860f79d39939cbdcabe2da719891bf9c63f72f5abdd4fa1c13fb5a0534e"
                            },
                            {
                                "filesize": 5633374,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "2cd27fc7058d31b2a7caec23c62e9930564e704a1d3bc9cc091783b34b8c078c5dd0ba2b90e7ab4b75337ef3dcc745a739eb000fe0ee138249670c5bb4b48408"
                            }
                        ]
                    },
                    "lij": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 41300795,
                                "from": "*",
                                "hashValue": "c96e7bf9f8fc690b43cd2f0fe04d4339c0a0c33a0b912ef2f445179532f22f3f70b0e3ea84a692e0b4a989ce4098bfd66deee5b5c212a1988e776022e3806776"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5542546,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "c6a52555e4534fcab7208051223ccac46d10e1ebc0cf4a88ffc7ef5188cacc5ad856985b7f8d0dfafa072f3e44531c37ad0e6ccff8f278235f77498117d3d13b"
                            },
                            {
                                "filesize": 5602418,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "88046fb861b0d13c13511ab8b817320d61e6e7918b768ef2e7f1995247a6fc63caba061fc48a0b0e53a212f52833e4e0026833b5c60e15a1237dcf5861da17a8"
                            },
                            {
                                "filesize": 5633390,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "32ac7d8271ff4edfde13b0974685e5e25f0cfae7dfad11e729e86feb701e43e01da5a1a713ff4c4dd6ba59ffc088d871c27b0fc365c100c7792ba861b33f3eb1"
                            }
                        ]
                    },
                    "lt": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 41403169,
                                "from": "*",
                                "hashValue": "1c5ad924ed79f9e5db1467c79682abf6725e62ef4efc024e9e7a0fd2e927b8578c045375716e67aec904b807ba78e01267c9f5710d1bb049bc284101c6392c05"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5542566,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "3c6b04609b54c2a1c8a67b5557b4765d68046f2e3719d3654c86f89e5f483baab4725f56ab0d63966206b5dd206b6038b46655f0637cd2d556706fe041b1fad5"
                            },
                            {
                                "filesize": 5602438,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "ebd3f30e9ff531ba4f03b3c66f82e5e201be84747a701e6cc18f2bd0588e5605380beb12af45657eaf6b806adcf5989620f77b02053f0410b593ea2a4ae35a9b"
                            },
                            {
                                "filesize": 5633398,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "b729a250a1f6ce8aa8c58da85da80a94e1afe466d01219d14ebf6538aa3c7f9a9be4b4e7971b7c4db8702e4be95443f49d2b0c26c6c5f5c68f3bddf3aba20ed6"
                            }
                        ]
                    },
                    "lv": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 41403639,
                                "from": "*",
                                "hashValue": "f57d049b895822ffdf37975f57df02c6905e25f31b2f6ec1abb8c09216a97244e8db81cf9afcf92b56551d48c1b213d770403f527b989874cbad7ebd3fb50e50"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5633398,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "48b6fb952efd433b06b2be91fdc29b260df2df5525f9bf19949f5bae6305d50197c01512fcd49b8ddf7066e3e56f6bd7ec70a9339e6005b583a0c565ca06dd14"
                            },
                            {
                                "filesize": 5602438,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "90d763658a8d001b7207a1b87eebac1dc8d99109206f5f6cfc78112315ff9d831fed53002d0d5d23c7840c8e62de470a548d2e26c9bf201f5bfabb28da1abdda"
                            },
                            {
                                "filesize": 5542562,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "80393e7be08882f3f3c714b9dcf960987e3a3ad58d05ac835196ce0a326997c73a90632dd569277ae82ab49cff51bc88a919bc4a5534a1fb98183dcef06a79cd"
                            }
                        ]
                    },
                    "mai": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 41138621,
                                "from": "*",
                                "hashValue": "b9a9fbdf7153917f4edd9a8279edb0e37559f4079d2d4eadd92fcfee03bb2b14c76734d1713ee6d27f409c8809faa273384faf27c9f8fb01c49fc0c521246d5a"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5633414,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "22a7d0b513aba4a43315ac0fbc13b02a64fbc9b725fb22b63057d09e4342bb03ca328780e49bce680a628c06aa5bf9543d158cea3fdd907d260841c4cbacb56a"
                            },
                            {
                                "filesize": 5602446,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "190c6038ff511636c39b21824e6cebdbc85a4c4ebd87b44b597acaf5606be78976cc139b2aba1f7782b4e6652ae8d5137d45c026207551e9055418a2e2abfbcf"
                            },
                            {
                                "filesize": 5542570,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "fb18bfb1bbb4ef0bad34b29934cc983b10bd2d6a7ae19ee9d4b412a657a8d53278649704502dca3728f2592f81b204e2a85664d59b4e7611d8d0231bd05536fa"
                            }
                        ]
                    },
                    "mk": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 41561701,
                                "from": "*",
                                "hashValue": "377d6569b91e96273f46bf143a68a8793429c48fa63f7fe4452a3bfe79074a2536c02628342ec7ff42e18fde681a0bab5cefb86f111e405d10aa44aa92a675ec"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5633414,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "526783c61b8b43f41562c4f91a6557b7a7234b2971a8e3d6cc7d2a5287a4f7ff84e87bb8d5a0ab239c3b18099dc7909483b9458343e90f58343d0e2340b5be36"
                            },
                            {
                                "filesize": 5602430,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "4de42b21a10ac67419ec2a82e3c42a3d268a0618307558cd750f4ab4bda1f58e5856c4865f9e6bbb04defea9239deaa238893eeb5df17dea65af9187f5ea2cbc"
                            },
                            {
                                "filesize": 5542550,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "ff775ddfb6949191e89a003aa02c0776384bc626a33f1f2df68d47d1f5df9cbea999fb85260061888c9b88a04a7f5cffbe4a15dc5292a2932431c56883e63696"
                            }
                        ]
                    },
                    "ml": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 41144777,
                                "from": "*",
                                "hashValue": "9323f1052ed2388d40e0c483818d8af71e32ba4e8b8070487f0e036f24ae8d51efe0aa7060fd1a04f992f998a1157fdef1fd581c65d107e9a5529279116e9c00"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5633450,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "d76a61e164019fbc25c01271c017a604580bf31d9cf1316d95b176a42d36f4fb86224f5a139d1ad9055823fa1456cb4bc4219f2df310df988d8c35b58511be9b"
                            },
                            {
                                "filesize": 5602482,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "298eb46f169d8d61f0fd95798c564441d3e46ef66fac07e18d019775cc462e6b63694727e638dd671a31f408fdb6fb8a73d93be20f166addd81295aa3bc7079b"
                            },
                            {
                                "filesize": 5542606,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "903c9d0a6f022352572139865bcf237b398f185e811292d37825472fda6e3bd383aaca470887994e876961cda43a657bc5c1db4dea5c90c9fd09f653a3e37a24"
                            }
                        ]
                    },
                    "mr": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 41139969,
                                "from": "*",
                                "hashValue": "2d5c9c7440038c1d2afa11a06cced48519129e5b9121387dd70948457456fbbcdd0d17770bba81677d2796bb979f5fecaed287b1724621765a2e0b63d50b8dd0"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5633430,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "c68dfc17ea9b3dd81b3ee8bb6f45364c1d370f01ca7a893861ce75e3b2d50996c45444b2e0e89be0b86f1373d55463e86c4567fda53c08e9fc58faf210621f3c"
                            },
                            {
                                "filesize": 5602474,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "6e9a51fc015ac6bf67f9fcf56bbfdfe010b7e6406392cd4f093092d8201d24b401cb3d31802e5a8688474d7dc400f080ba3f317606a9a09db670459e339093f9"
                            },
                            {
                                "filesize": 5542602,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "8860e16afe51e7b78a5622bdbc5bd8be110c0c0f74a5b4658e3b9a5e8c43defe698dc77981f2c0a73187cc0fc3390e7e6f0ca4af9b8f4be4ad0bdbc94864c99c"
                            }
                        ]
                    },
                    "ms": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 41119541,
                                "from": "*",
                                "hashValue": "e29b8fec41a7801f5ee2f7f5d3de86c8c497eea42fe4a1283cd294d3491d45fda46d7a475870e6a7c863fd76cdedc004f226babb9bf23352e44edfbd892b380b"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5633374,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "37024a8f623e77497ca0dbb693621330255f0a6fe5a9dba6f8c08be097e6e1c6e9e93271b84d135137f378cd3859a72ef1a202ad393656a6c4005b2ada4de896"
                            },
                            {
                                "filesize": 5602422,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "25eba05b354faaefa470456840a7c98e9eb8081f1d59406c0899542192691ad36e7ce2300c79eef9befe6107ddaa22e67a5164a4797ff7128d9438d319b90ed9"
                            },
                            {
                                "filesize": 5542550,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "ba10953166d899798973f8d94be2c43732e7ebd39dd397230bb9da7ab440f54967994792032f10341026618571355aecbc6055440212f88267f8295852634e1e"
                            }
                        ]
                    },
                    "my": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 41143565,
                                "from": "*",
                                "hashValue": "049ff1094d348f6c384f1ef4f4f77da4b1440c1ec72c4049f5557667c87b92003fc4e04d06c937e640c606ebd8adb1c8c994c1946e7b69c9ca928f89d91828b6"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5633438,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "0598a0d50183251516f5d509072411138a0facdb2a6b4061f5b2e112f1eca4c04e84451d8871fd71090d31e4fc31da91a39993e72737ebfe758a6b1bccbd1445"
                            },
                            {
                                "filesize": 5602458,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "17db1a01d54dadd21b653be1b8f68f176691d82f2d66ccf973a801e1376f1daa0224a85b38635be4ce5b380aeed83c33462b06093b8e85c67249d43050999c6c"
                            },
                            {
                                "filesize": 5542582,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "fb39ac2cef932be3de7ccb14578445f052c1a608929ac861ab86e9153a041548d6c10f21a5dea67566060325ec85a5af60e41c5c0b614da3a503adef19dff21d"
                            }
                        ]
                    },
                    "nb-NO": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 41117705,
                                "from": "*",
                                "hashValue": "479c8f8e301a1317664cafd0013399708238491a32dcbc2d8ebc847e72d71efaab10b5fcbb312829007096fd077f776c7c012d5a43cde03c19ee13d269f017fe"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5633374,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "7fc7dce2944121f96e912ef4ef3c97b62dca459a2f7bb0f973abbb08249a8e9961801e6d3507080d351bbabbe1fe6f9d9fccd1cd5dbbf688f27521f3a9b97b95"
                            },
                            {
                                "filesize": 5602386,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "ffa1bc8876fcef6eebe4a2aa01ea4bcc58b5e03e9dc9f665791f773554ba7aa468de2b8b703428acf33f878a0447ff31b183a340ac1dbf050e30ce6aca143aed"
                            },
                            {
                                "filesize": 5542506,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "e320c696011566afeef9fe5d18294136a326b248941e81130d56fddcb743819854a2d8edb41ee86d9ef4eb3d530763859b7ecbc1336da68556f11778b2e985c1"
                            }
                        ]
                    },
                    "nl": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 41792549,
                                "from": "*",
                                "hashValue": "c1c85c5f1a823f976d43eec44deead6aa2f8065b0207aa526a249711d58541f13e50cb32e03ffbe2aabea7eb22cd2c5410d99b9403225b981a5026bab2546d3c"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5633398,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "0f245ca5010c48a2ede2a4cb575205714b62aa67594739bc7eebde8b53b6f72a7610a7c36641cb0081cf64fa752447a3bec2a3b808a22daeae8cff7f2adbcbae"
                            },
                            {
                                "filesize": 5602430,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "f3c9476c54299eb249196bc11bb9ae2677f6dd9c7a78ab99d242cddbc3be4e2d1c8961dcf870b8cb5a1b6ad2079f0d27b5dcbe8a25d3749d2c827657776d88d5"
                            },
                            {
                                "filesize": 5542550,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "0f493a3af1cb6408a82b8ed719b674ac37bc6ffc08b15da3fa444d5e7a48dc84ce32c2c7022249a0cdeb4dede81754882d6c60989029dba0f12876203a2cc37a"
                            }
                        ]
                    },
                    "nn-NO": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 41119941,
                                "from": "*",
                                "hashValue": "93f1f6f4bdf3708342e9bfbe1a47e3f428474f2f62eb95ec8c30353a075bdb8c7c0b1cc1dc27d88e7bde22e74ba2de3648eb7d95c26ed3e858de52f4d93d3522"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5542506,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "7d85adce1a712a8019dfd11e155753783c3455230abb01649a92ee8183bbb611e1d024050e10b6c41ed68f7183232aeddd2bda8281dfbcc95ba4dca170d4e253"
                            },
                            {
                                "filesize": 5602390,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "ff2f0fe4c5eaca3b84e1f4d4c8a91f7930a9be7842dd984d00868164bfa3372c17caaba80025764a03f3eab40b8a300dd5981507bb7a48e919a8a9681c3dc39c"
                            },
                            {
                                "filesize": 5633366,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "9c4fc2b3e4460dd38f8a854939d535bfcd9c4604601b7a79bfa9c36d33197b96bc7a031172cb220a7c2736ae2c4fcf3b837447353e5b037c968b50b9f9ea6b77"
                            }
                        ]
                    },
                    "or": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 41306839,
                                "from": "*",
                                "hashValue": "c49923527ab8290556a2231b8acbac5779cb4facbcc557029fee66bbeb54e2a8ceadad4e5a81bfc6a4038aab959e89c262d138d39426d36d8826d794ec337b64"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5542594,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "a1e95c7ba687003d6f993ed0a8158d30351c3b626378a42cc62e04e9657a8fc78ed94840e591c03e10b979bfb2f55f65374daaf8c0d475fa9bb27f1ef95727ff"
                            },
                            {
                                "filesize": 5602470,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "85990a2833cbaca7e9ec069b82beb06427748c5b2823efe3e57e4267f2c5a95b9b4c2294975eef550908ed71b8ce4cab96b6779d594e904de67a1f72b96719bb"
                            },
                            {
                                "filesize": 5633434,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "08cb5ea3391c3b562aaaa6da37d7972723c3fb67d78922f6b84e2bba0e26a86b2b823e20306febbca1930d0a29908b50a02b0c67fb16b1b8b5d167fde8a09385"
                            }
                        ]
                    },
                    "pa-IN": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 41127473,
                                "from": "*",
                                "hashValue": "990f056c520c89e28edd0e49e8749a5a376ee4c83f4fa80e707326229f6505090d8d32fa0f94a54b05d2261230a25749f620ed6a04f560c8e12e3f1bc2a19e0c"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5542554,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "77bdf8cae639b893e5ec7aef298d8f809191d3c4281bec0b875744a0c5632eea1a62409fb2d1c812576d46804d17f6e9913e43348398e404b209d4069cfe638e"
                            },
                            {
                                "filesize": 5602430,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "d6f78746e05ba23996635d93715ff6467c373ca0854efbe6e976f5c3fe1b3c055fe448f34559a0c0c5492e85d66f4ba63b529e1a103135c2bf94d3bd97af3805"
                            },
                            {
                                "filesize": 5633410,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "b2f45272744f0afe004015dd2b2f7475b837a5ff4346c710b9e18e3775df588551409702bcfeed887691b50385e2439543c5f6107963450d51b307270ca593d8"
                            }
                        ]
                    },
                    "pl": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 42041029,
                                "from": "*",
                                "hashValue": "7e8083584168326f0f4e0dc681b2c8e3e99a9699297031cd6eb76a854d65dfad03d9a4d60804a64dd857473c1124edee7b6b66f2448bcf838119a48fac0b984b"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5542478,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "99c2b76baa68dce98b9a45524011b66e94ec954e354eaf903a4367d211f0397c715c12e66f2fb1145f3049a7e0263f462621edc5082350bad3cb824e62320029"
                            },
                            {
                                "filesize": 5602354,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "9f2a2c8da7f50e0c1672df3c484c2a12703d7ecd722b1429d2e3f074a27d1ea12177ec6e96573c14f9a6a2e39650b5a31f8a265de0aaf8eba95d02d9dc92571e"
                            },
                            {
                                "filesize": 5633330,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "a6157d4f7c1f580fb34dbe02d57e01740dfaf9e98a7e3c175aa1b59c733adc20d161ea90c1523d572f73faae65f0c861e9fafb88d23136827f570a045ac93906"
                            }
                        ]
                    },
                    "pt-BR": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 41272583,
                                "from": "*",
                                "hashValue": "42efe096e107af1d37700b9c53b5c86697210c1b3648822b4ab4e078169fc839546f769a779cc8e16b9ce64cd2e77a366587deaf17f754fce1f8213a00b6285b"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5542566,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "5d59c5dcb55fb1cf4dc836d7ea305e2ceac1508f041465c7ce5b91664b3aad41c66dde7da35a20084c3ce18db9bf7a20675a34e8f4c2ba3baa3c85b04bf6da9d"
                            },
                            {
                                "filesize": 5602442,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "70793e4878b500f24ab61d129645da8db175a408cb2c80deac77e6f4410fc88be30e2b19624cb36e20876e32da1f95cc8e2e96caea628659b4bc75f1e9b8b993"
                            },
                            {
                                "filesize": 5633394,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "23b2f23c9392e6efce8eea3446ff4bfec816b1e070409b472ecbb9e6c9ab9de8fe9909b44cc2c3d3d4a16165e2cb7dfcaf87291e584897788945994c25b39903"
                            }
                        ]
                    },
                    "pt-PT": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 41297851,
                                "from": "*",
                                "hashValue": "be40a1c7e63cc967a9dbfca8c08db2d95124e472bb6736c10e0a7cd1f6ad8f981a5b95306a72046b5721017c8968826c7cea9a8ec19d3e4a21a63a21b2e69d74"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5542546,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "a45cc6aa5a87ff061cfea272cd86a58632f3a13c18dce1df3ad272008fb01dde8e3596fd05117bbfe9c2fd231d94e2c1bba4d033d4e59857ceb59b3105fbc4b0"
                            },
                            {
                                "filesize": 5602422,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "dd308d478d370f56382315dbf22c3dd34ea5bd046e6d3d3f5c68bf8c18e7b655cb8446cda33def439f4dfe87895fe357d5f9ceb98192ea12065aaa07f71c5465"
                            },
                            {
                                "filesize": 5633402,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "aaa878cb19409cce1b1e9ba3bf3d24801d281f709dc8f9f870813770068dcb87ef827fa87cf09ffe3f0e770f54c5258133b1cfe7d8cd8c3a75f2942fdcf71ddb"
                            }
                        ]
                    },
                    "rm": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 41305897,
                                "from": "*",
                                "hashValue": "e46d902ac4d259249c3d607fd63e8ce6b90071a3c01983c9ca2a4c90f6a54e18f2a40f9287ee746d4debf700d92299ac95eca706e4231a7c076fb143dcdd01cd"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5542566,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "69283da7ea5414734bd9c187c8a2df4529a9a1bc78ba1953893bb236ec785d3fcc5700804d9f593727d9b015cfa2df5defe1a94f25db64b6bb71c3b14ff79d67"
                            },
                            {
                                "filesize": 5602438,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "097980f9cb0f4df463b91a9d356d149f83fb8ad4df4d5781cf40c63b971ff6420133b23cf2074aa3379634d1cc9ba130fdd0dad452715dde815f3d06a1031853"
                            },
                            {
                                "filesize": 5633406,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "836abf258fb6e4c85d966760e6b16c3610b2c9ebde59456c22cf98de4f8c0f62a601abac34002ceaf551545d43298393dee2ebf16af4a9910ebb06fd8393106b"
                            }
                        ]
                    },
                    "ro": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 41608921,
                                "from": "*",
                                "hashValue": "3303d6ae89bc9d91d672464bc76960e6bffdd573be21e56edaf019ce9242e007af095e78814d7c6c16bcf62f3cbcdcf89696f41bf4a056a77d040f2e0b57c3ae"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5542562,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "3d8761dc41ba73b9143d39d74a2450eb70e162bececeb3d8b672c95af426b13ceca3f5fceeb071ad45db70b24664f19948a5a7b570a4f6a06ae4e5fccda4730e"
                            },
                            {
                                "filesize": 5602442,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "df229bc3005a0d41f0dca0b5fa894caec2229e6f1a0d7a938c8733ac795938a8917301003f2e65b87f6125478c375c4b56dd5f119d98a4ba267f6ef59a624270"
                            },
                            {
                                "filesize": 5633394,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "36b9558df8ef44126c509baf28f919193bb8dd07f70dddeb943c518472e9ab4e3772a5158901675319168d88cf04d4124284ae9df2be57cd6378f9430ac3b4c3"
                            }
                        ]
                    },
                    "ru": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 41564561,
                                "from": "*",
                                "hashValue": "7d7cfebc40b26c0a1093f5865184b5db50dcc09ad712b3c7801530f45629ec869d00b661859add6ba2aaf0e4356b0e755537cb5ea39683195c5ca0eff5aa03fd"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5545534,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "5ea539fb6d0ac68c74975ca6f959e1793d0ed6dfdca9fd8c7ad6a1a14bdce3221520e8a022ded79d2f6f5f4523dff26c17c2eca777179732d1002d5fed789090"
                            },
                            {
                                "filesize": 5605418,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "10adcc5641420c7cf1c2db24fc45b2f73bfa93c90c5ff3fcda073fe4fa46b3767c0fa86b11c7bb4ddc86510e795939d15661b75549142245adec720a91ddbf67"
                            },
                            {
                                "filesize": 5640106,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "d884abae86b3142d0359e0af432a0c004d8547f93fd9f7da10d38ca27e1ed60a05e6ef3118cd558f64de278ff79cff040fef80990b7b5944dffced6e4b733b5d"
                            }
                        ]
                    },
                    "si": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 41130933,
                                "from": "*",
                                "hashValue": "a0ec95be138e09ff98ceac1cadb087173189b5941a5522172e1ab88728469025b48b1850f0e5b93d002162065e36cb2ebc07ed787acd03fa59a3938f9c7cdc14"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5602414,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "2e068eba8732d590d49084b14a83c577c263aef6d6b247f778f79645bf0b922bb703db55157161ec8bd73108c5d8a2c407bbd811a121dffdad8dc9905022d159"
                            },
                            {
                                "filesize": 5633410,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "7dedf8e8a5f0b3eb8090954fd421015bad8a8be0cfbeed0ed76acfcf445711c50158e086a8b7d1eba978305942427b66abc48416596a5af381d48f27907d81f3"
                            },
                            {
                                "filesize": 5542538,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "b1adfe4c6d00d6324dd9b941802318ce0b39ee1eba88b6027c7a308466d6bd8370344f14b9682c814237d7ed55f4582f9af13a6c3768cdbe7e499341df46216d"
                            }
                        ]
                    },
                    "sk": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 41816233,
                                "from": "*",
                                "hashValue": "6fa4b0fafdc485d04c38e351e80df4c852f30579779189cf9fac81d182f11b53f91916acdd135177a436f5b183537d16794df6ddaf3ea2c32e96443672ac547e"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5602430,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "a99a3e17f418470b6cef372fb281f6069b23ea676922172d1931da5549e8cf99c5f95ccf254f479257e647573bbec2685db5405e36849a6da7960131979a2167"
                            },
                            {
                                "filesize": 5633410,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "450f1cd1444b07ad636d9d377f30cd690fccb6da8e89ff9df91d13a82ebd86b7b4afe52aa73b1fb07e53818a5ea7a01465b281556fe16accafbff1285edfb08e"
                            },
                            {
                                "filesize": 5542550,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "91fbfa126039dfd19a6655c92dc903b059b812bfb3bcf7b213cbff21b596ea186388798ee1dec3db4d33db56858ac153a2bfa79d21aae50668ca44985349ff1f"
                            }
                        ]
                    },
                    "sl": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 41126817,
                                "from": "*",
                                "hashValue": "41a27dfef263487fd7ee825e2b744d5b0f4c2f63d7c765202d24097df120d5432de5df956b9bd20f37d23881e05da792ebcc7b93d9408aba46216b123bd080b4"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5602386,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "1b2ed8fca751e48c8b6bbb35e81783332b5647f93d6e24714249a7b49e5bce17376e7576e22fe69a0e26d86fb4e74efb6555fb6052b15afed5ce3a2dcad5fa6b"
                            },
                            {
                                "filesize": 5633390,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "93369d0e84580663de9575081a419bb2b0356fb22e438541fa79e19b29c55098ae7f8348c64dc229d7e8a0b443367c62e46417aa53f7c04a76e38bea1ff21b1e"
                            },
                            {
                                "filesize": 5542510,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "855d37cd3ded093eb2a24be6932e12155668d91524f6555857f6cf2e829cf17072d09a0b19886701769a248bd6ba8078ce33fc8518f9f3ce2a58ba7aa5bc6bb4"
                            }
                        ]
                    },
                    "son": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 41118117,
                                "from": "*",
                                "hashValue": "34d3a3cbe85fe7defc3ebd224ddc28f2bcaf7528fc8225ca58e70a821a23170819627faa61c119c601d0b92b02a70d894900c8c26bdac891a8801d0b7c60ced2"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5602398,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "9d102635d780bbf86932b890fe8952b23f354f37435c7a1009ee5acf607c297b83f86270a794166468cb5dfc2b8448b131954fe57c52704d85ee1888d40c458e"
                            },
                            {
                                "filesize": 5633382,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "a4ff2bf578e512a30aed91a1ec434dfd1617754ffd76f54706d0ef71efa27017d25c2e26b92b831762c7c7e1a1d67e34c2e10976b3c3a7bc4deefa735bdb7a33"
                            },
                            {
                                "filesize": 5542518,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "d9f521ce7d9bbafc8ccad7a35c3613e990a83bc0e94c222d5571b04ab01620e6295725c9651874956c0a4d11e16071a7737d3a754e03d2d04a7acdb1ca4778b1"
                            }
                        ]
                    },
                    "sq": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 41130713,
                                "from": "*",
                                "hashValue": "52169c222815d5ebfb3810cfb0de761c238f0b2daee43498ad05e15f1fdf01287749bef013732882517b5f54816622842b50f5e9d1361eb780a3015159d9cef7"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5602402,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "06e631fd03297789b2e21796e12cb9b441ae30dcdaf1c667380671d823af7e432ed4fd80b6c413d1c671466226a04aa325a0b7c76998bbbe96d2d854619120ba"
                            },
                            {
                                "filesize": 5633382,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "a51107060fe850a537c48f3e8e765898b3bf648e938981bb9299ea5592c237b0ecf6ffec29629c41b323a893a2dc280f3c7646e25250f2186a2e2a388bc45d01"
                            },
                            {
                                "filesize": 5542522,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "47927cda4016102122618a4f672df3ec21e07fbd4027876c7c6a5529181acb9e8675ccb8cc2a36d2c8c6f7c5cb185ffad496fa2820188b76a3cb49fc201c954a"
                            }
                        ]
                    },
                    "sr": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 42251765,
                                "from": "*",
                                "hashValue": "8648ca74ab71530291b1552bc1a6095b5ba33b056837b4f868c94ce011f609cec39dc49d9f880e3fefb0a1ba5bdae472ee83f171a1adbecf59d634905fba9699"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5602458,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "377daa2d7acb0cedca4ab8cfee0668e798be0199c7307f8ebc3dbd1786c75ff33b33e9916e405d7de39008f493ff6b12ae3ca18e61c880fd6e4cfe12e265c021"
                            },
                            {
                                "filesize": 5633434,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "b199cd820e3123fc020f1cf923e7ec4a6957a6d7939fed249d6d4e42f6e43a40cc7e1cdefce04d4937d96897f85ac985da81fcd78ee12d79d00a65dc48d6c37a"
                            },
                            {
                                "filesize": 5542582,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "917a602c13574e83cb2eb85956d85368bd26dfc64f0399e4ac05ead986116e1a9fcaf35828a5fb58e29d42e23dce8d5ed882f571c1867aaded977251e2fb8a82"
                            }
                        ]
                    },
                    "sv-SE": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 41663001,
                                "from": "*",
                                "hashValue": "1db0efb14e64a9b7fcbad6ad008f00c218d34cc1822112fe87d577422e10c9f8b779ef536e3056744212a97922f211146c8762acdfd75339928e090e49d57514"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5602438,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "b89ceb621b877b805d427dcbabd9c3bc525cec6316282519a35d819119c6a334f7b4107383477d7d402d05ec9ce745f2ea594225aedbb5fa3883dda9d1252b15"
                            },
                            {
                                "filesize": 5633406,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "d424214a38b9f4931864eca14cfc8c4d690056174d8e2773f0c8f1004c3eb203813bc6cd0b62521e0953c49555e950fa0e695eca4b620c43e5c4f80a4eab7c25"
                            },
                            {
                                "filesize": 5542562,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "3b7ee6e36f2f7902670425c92c5677a17eaa29986ba02746fdc08935f63e989fb8473d5f3078e193dea328d92df2de2c9cafdfa0422d889d840f9e47a8358f0d"
                            }
                        ]
                    },
                    "ta": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 41340511,
                                "from": "*",
                                "hashValue": "c6a78e07f898485d53a5f92846240ce8ab7ab7c88d90d4c2e166e4ed8adee5ad7f56fc62a3437c2755f730b9804117c884540948927883bbec2cbebeade4404d"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5602490,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "d5e0d1e433b6f85676be5a6d211007df6b5dabab96a579ef58fe6c8140c64e97d9cfee3d6a47bbdc597289d4695ed4a67191622ae230ea7b00407727022eeb21"
                            },
                            {
                                "filesize": 5633478,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "881d49f5b6eeeaccd338e0f093062d16451740cab9a7ac3eccedeb69b4b86a46b4f890fc44be17122f9f36d840df44e27e5da687a1eac7b5c9957f051817da10"
                            },
                            {
                                "filesize": 5542610,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "1ee104fad9874a15ffe2991067abc0ad289a691ef981e8b7bc3db93d9a9a13fb100b853468ac67d9ce4ccb505438f73fb70a003e561283ddbcf7138540d13789"
                            }
                        ]
                    },
                    "te": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 41145701,
                                "from": "*",
                                "hashValue": "f52c8a2775baaaabfbefe0e7803b3ea666dd44832dbf92674b889cf755ed97e60a387e5792ab1c88d28f8a7589651c87b3289e93ff66ae13e26c35eaa3037259"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5602482,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "d0873a960d31e8616be5d5833839fa829e8b336d0827fedd66a7e52b8fef64ec9391ffe7800381aff36dfcaa09ee7b9b002530e0b860d62c495208dadd68fb28"
                            },
                            {
                                "filesize": 5633450,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "48de13d91d7a3ccf89f3a2afea468bbde2cd95307880dded13741a8a3de32d43ed9e24a565228f3786510f6d419871e932cbc4cb12eb83317bdb5d816ae88439"
                            },
                            {
                                "filesize": 5542598,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "a06fc47d54549914ba7d90f0892b37bee6b897362bb8a0850427e4749723ca88b9ec8a6a45533bd887f6bef0a3c639c56dcdbecc712fe526284bd7a10548942a"
                            }
                        ]
                    },
                    "th": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 41125377,
                                "from": "*",
                                "hashValue": "eb21edd21bb1ac3f0abaca857031430b16f33ed136689c1197f9036d3de709c556ad8eb67d461c3d2f6f39af80044f1df397d077802e46e1e464ea9c9199b9d2"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5633410,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "e38ddbbbe3055fb1bd98f2d3483105041dcb112f2cb8e1f026c16cd6f740da11520ccc4d59cc1b74f756e19930972d615c1100d1531062d28f63a36e14ec0cfe"
                            },
                            {
                                "filesize": 5542554,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "548a83b5611a0d735d95be2a0d1d54f1d1ba82d4feee9f7e572c3428b70ed8d1944104508c64274410559fe4e37382c8600f154da88ebbd7eb4d542bc73b90f0"
                            },
                            {
                                "filesize": 5602446,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "b1d4d910b67b334f27751ab9d23c29790fb4970c1420f560a7ca273996b5f12aa880f09cb392347dd0c0b1577005822360d4aa064b381cc62dced7ab428e2d1e"
                            }
                        ]
                    },
                    "tr": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 41124585,
                                "from": "*",
                                "hashValue": "bdfce5b4a1c661f7db6e51676d83477f81f673162b9a8ac8ffc2e240f3fbeb22a6f258b8de64fd636934f41048676f91dfb0725441089315e177e6bf403753a7"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5633374,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "e7036d172c65a26a1e55a4d9bc99cc88fefb2426c914d9ba9d3de1302711cdcf890d68437eebe9686a984c90d17a94ddd9298344a88bb09054a35f2cdb01c099"
                            },
                            {
                                "filesize": 5542510,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "f85ee1e3057f884ed5d11e48c70a8931ebc40a162195f3c3fe8cd7dd30070c15448ea08fdeae645f60b4974692045e071f3daeba748f7463ad7540a1e7500b10"
                            },
                            {
                                "filesize": 5602398,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "87789c22b8688c22492a6e8c16155d4f61fb398cb0e102d7d00c33326f7bd6fd57d4b5732977aab89ea40127c970db9df912938ccf72334d8c76fe276fe9ec97"
                            }
                        ]
                    },
                    "uk": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 42012637,
                                "from": "*",
                                "hashValue": "c51991a8380dcc4e249d512f908716c618e2524d8bac1f7f812a04ff6aac16fbae09356c84fd80d406159738f9b990f6e900eb18936e398acb54075dd2a02aa1"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5633426,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "229696d14e8b37c13d3a3f64ab2b2bc4ebc78111dc8abb11fe7002f9dcc0ad0bc4cd17665c3ba5918ee8813b20b3e3c8df92729dc25df2940a1d0729413921d5"
                            },
                            {
                                "filesize": 5542598,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "d9496cf512a17cf69f2bcd2cbaf9a1824728ddb791650e07b017fb2d4c3ef5823553cdc14da04d2d11d3c3e82b7d5e45e62b4034089527cd4b6ed2bd7d2580ff"
                            },
                            {
                                "filesize": 5602490,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "2c24c07762feeb6455b5f98b35a73078283aefc721393794b9389a44bb2b815e3bce721162cbc59e6cb76de0c8a54805482f543eb0a9c84cfc124160c3f7ce73"
                            }
                        ]
                    },
                    "ur": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 41143925,
                                "from": "*",
                                "hashValue": "97b6b9ccf6fd570842a817b81ca89d4a2796f9cf6629a2ca9848e0e4a781ec22b1b865bdd999192844ea1903abc143128853e63ac2bab3ca1cc156b4655f9eb3"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5633402,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "18d45dc3638e088652218d2992cb7309623c6fac9148fb2cac4a5b079c37a432f4673002c757cf20d744403ed205630f5df328ff57cbfd9a91a855ac471e4c4f"
                            },
                            {
                                "filesize": 5542550,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "82a435c935db72465c7a2559c4a83d6df47555c0dac279dcfb524b761879960281bf74459e5f1bb09dbb03b9abfb263391137749dd62eddf1386ac6a86d97db5"
                            },
                            {
                                "filesize": 5602438,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "1069ff61cfafbbf205b879398efa344acc6bca0c3c20e8a6bdd093d3ca35ee7ad19e233730e052d2f112889bdb959abc273b3c59ba5a283faf10728af8a46288"
                            }
                        ]
                    },
                    "uz": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 41124313,
                                "from": "*",
                                "hashValue": "3ca6b339ab3f98f5f2dd9f4364b53935bab18353d0c7b1ba8f9d4084060758ca0bf25cf516e4478805c299cd130a074752d48691a4fa117b02ea2d80d6969891"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5633382,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "116568d29bac1ef26f964a1a79953b7e02ead5cff991b6c7cbd92ff2b2290c253cceff8fc57253e3606838735ad6795d91676b83ed44f0c4560d4f7f3daf74a6"
                            },
                            {
                                "filesize": 5542538,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "1c962f3c7c2684807bbd9d646dd2ee561e1c224d9e8841938ddf3120bd72ced62f3b0929176107cbd54fd048c603b2816c008a7a5a8c4e1a903ed2cac17ea5d5"
                            },
                            {
                                "filesize": 5602434,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "cd13bce96f3c5114637bb2e82fcb284d1782862696de7c5a7796e27e7afbfff397c3a385576e6fc4bc738e9d6f5b80737812d5e5c197745b1713ee4e27a10631"
                            }
                        ]
                    },
                    "vi": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 41137317,
                                "from": "*",
                                "hashValue": "89207dab7bb3c9ba93442236fb87e6feb5a2edb23855dbc5ca7e5fd4578f4410d2ce89983e7146063690077fd3be1e3ddd89a3a0273f5d7ebc4d985ae40f8342"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5633426,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "0380b5da8d259e77c06b1474c843ff29c13eba9f671b1fa50681cbaaa5d197543b8950dc6519a571ca772300950e09f6b70d425bdb074726ed96c82eb87cfbcf"
                            },
                            {
                                "filesize": 5542578,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "901a921ce59ff95bd94919d43ddea07d371a6d75e05c97e9903ab60a790cf4d1895c03fabef2082a3b3e73d863392b39dc0b89800ea2edbc890c70de28386331"
                            },
                            {
                                "filesize": 5602466,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "dca81757b3989d2b3c6fd428e1443870dc2454c779b87f78ae4184a8b48a9c72b80c7ff495c1daafcc54e9dfc3ea89c3aa7cd61414f8bc375838aa7a67b96553"
                            }
                        ]
                    },
                    "xh": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 41132405,
                                "from": "*",
                                "hashValue": "54db592d7b7bcbc90188ea7e5d8ccbee7074e83f1ec42aef3fd39d67668d2826e12c8b9597cc1afdf27e75efc507a8eaf3fe6f44398a65616de9435bac55694e"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5633370,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "ee848fbc8f491342d07bbf883250f9a2008475687c48e804a34335aa87f0fa67f18fbaba43b686cdd793b6a9555e12376a9954199e3eb0f06787695287e94051"
                            },
                            {
                                "filesize": 5542538,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "5c82002c4de1de569dcd306e711abebc983c34e99dcf7c189db59904aa049f9d8bf69608c808e6aaa90f3685eb911b8b655dec5577dc1575227bff6b2902b338"
                            },
                            {
                                "filesize": 5602422,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "92d1a3853e3095c5017bb96779775e6a11ac1aaf416d4c55a0f6030d0dfe6d3b3d00e1503d0227ebcc8f0b9d698ab456c5cf0df0bd94cf5c7ef1dceb65816d28"
                            }
                        ]
                    },
                    "zh-CN": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 41122309,
                                "from": "*",
                                "hashValue": "9fc609e7607aac785d69aa962068e6dd832bbac3b9e0c353a855ea058b643851834d0aeaf73461d9f8cd499812898e10da829437d1409637f9c6d9ac5c5f9e25"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5633374,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "8f89a638bab5edffc5e887100a462ac56a12742c4e78b2d3baf39e6fc7dc7a393d4460b29c74c1fd61c57dc1f95a263b9a7e71b72b47203ebdd5886b1df21901"
                            },
                            {
                                "filesize": 5542538,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "4d0a1f7bb4a937539390b9caa5df94c25173aab07509bb59d5091897934729c877507314a6123ba7acfcf865ae9b84b19e9598495c9fac58dab1cc8d6be39adc"
                            },
                            {
                                "filesize": 5602426,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "3a22fcb670929aedc3f77ff61df99f1e52578c9135d33e23f03792771d2c77a491b982fc45bdd119b4f4ecca0018ccc2b5490f3c2e11398468e28e23a625ff75"
                            }
                        ]
                    },
                    "zh-TW": {
                        "buildID": "20180103231032",
                        "completes": [
                            {
                                "filesize": 41296195,
                                "from": "*",
                                "hashValue": "ca4fe9e652e89ec42ba1374d8d58d85f1fd8d136173cabac44d4962e4e696915cddab013723809fcb7c25c0d93a4f7b20bca9106a0ac43077ac61e3ec77fa743"
                            }
                        ],
                        "partials": [
                            {
                                "filesize": 5637626,
                                "from": "Firefox-57.0.3-build1",
                                "hashValue": "2950533ac53bb7e5570294c2d93fb6665d2acbb8b3f2a9fcea9f6f40790c9c49eeb056f68999d7ec958b0bbabecfb1735419505f1b5b136d69f5c5cd1dc5f8ca"
                            },
                            {
                                "filesize": 5542962,
                                "from": "Firefox-57.0.1-build2",
                                "hashValue": "028793faebcc31ec95848efc55442f22691821509cbc32e27c1dc782d8ac6f970ac2f43fa37b6afe4d5357cd0e9c786c09dd997a0b3a8b78142a1f1ce08f8cf7"
                            },
                            {
                                "filesize": 5602858,
                                "from": "Firefox-57.0.2-build2",
                                "hashValue": "92088686fcc001156b366dced51fc59ab87fd655971d7b06694c851a97aeaf3ff5369bddaff8100417ade095964c2e2099ad87044611578128c32cb7ec1da702"
                            }
                        ]
                    }
                }
            },
            "WINNT_x86_64-msvc-x64": {
                "alias": "WINNT_x86_64-msvc"
            }
        }
    }
