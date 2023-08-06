<template><div>
  <v-form
    ref="form"
  >
    <v-text-field
      v-model="comment"
      label="Comment"
      required
    ></v-text-field>

    <v-btn
      color="success"
      class="mr-4"
      @click="startScan"
    >
      Check in
    </v-btn>
  </v-form>
  <v-card class="mx-auto">
    <v-alert :color="status.color">
      {{ status.message }}
    </v-alert>
  <v-card class="mx-auto">
    <v-alert v-for="(checkIn, i) in checkIns" :key="i" :color="checkIn.color">
      {{ checkIn.message }}
    </v-alert>
  </v-card>
</div></template>

<script>
  import gql from "graphql-tag";

  export default {
    data () {
      return {
        comment: "",
        status: {
          "color": "blue-grey",
          "message": "Scan not started",
        },
        checkIns: new Array(),
      }
    },
    methods: {
      checkIn (data, statusObject) {
        this.$apollo.mutate({
          mutation: gql`mutation ($eventSlug:String!, $personId:Int!, $comment:String!, $lat:Int, $lon:Int) {
            checkpointCheckIn(eventSlug:$eventSlug, personId:$personId, comment:$comment, lat:$lat, lon:$lon){
              checkpoint {
                id
              }
            }
          }`,
          variables: {
            "eventSlug": this.$route.params.slug,
            "personId": data.id,
            "comment": this.comment
	  }
	}).then((data) => {
          statusObject.message = `Checked in ${data.user.username}`;
          statusObject.color = "green";
	}).catch((error) => {
          statusObject.message = `Error checking in ${data.user.username}`;
          statusObject.color = "red";
	})
      },
      startScan() {
        try {
          const ndef = new NDEFReader();
          ndef.scan().then(() => {
            this.status.color = "blue-grey";
            this.status.message = "Scanning...";
            ndef.addEventListener("readingerror", (err) => {
              // FIXME use semantic colors/types
              this.status.color = "red";
              this.status.message = err;
            });
            ndef.addEventListener("reading", (e) => {
              const message = e.message;
              const checkInStatus = {
                "color": "blue-grey",
                "message": "Decoding...",
              };
              this.checkIns.unshift(checkInStatus);
              for (const record of message.records) {
                if (record.recordType !== "url") {
                  checkInStatus.message = "Found non-URL";
                  continue;
                }
                const decoder = new TextDecoder();
                const url = decoder.decode(record.data);
                // FIXME use configured base URL here
                if (!url.startsWith("https://ticdesk.teckids.org/o/")) {
                  checkInStatus.message = "Found invalid URL";
                  checkInStatus.color = "red";
                  break;
                }
                fetch(url).then((res) => res.json()).then((data) => {
                  checkInStatus.message = `Checking in ${data.user.username}...`;
                  checkInStatus.color = "orange";
                  this.checkIn(data, checkInStatus);
                }).catch((error) => {
                  checkInStatus.message = "Error retrieving or decoding data";
                  checkInStatus.color = "red";
                });
              }
            });
          });
        } catch {
          console.log("Error");
        }
      }
    },
  }
</script>
