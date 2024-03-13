import axios from "axios";

export const ServiceRunningCheck = async ({
  dispatchFlashbarNotification,
  NotificationConstants,
}) => {
  const requestURL = `http://localhost:5000/`;

  try {
    const response = await axios.get(requestURL);

    if (response.status >= 200 && response.status < 300) {
      dispatchFlashbarNotification({
        type: NotificationConstants.PUSH_NOTIFICATION,
        payload: {
          id: "service-running-notification",
          content: "Service is running successfully!",
        },
      });
    }
  } catch (error) {
    dispatchFlashbarNotification({
      type: NotificationConstants.PUSH_NOTIFICATION,
      payload: {
        id: "service-running-notification",
        content: "Service is running unsuccessfully!",
      },
    });
  }
};

export const getNextFourTrains = async () => {
  const requestURL = `http://localhost:5000/trains/next_four`;
  const response = await axios
    .get(requestURL)
    .then((res) => {
      return res;
    })
    .catch((error) => {
      return error;
    });

  return response.data;
};

const createFlashbarMessage = (
  uniqueIDAnchor,
  type,
  ticket,
  content,
  dismissNotification,
  loading = false,
) => {
  return {
    type: type,
    id: `${ticket.ticket_id}-${uniqueIDAnchor}`,
    dismissible: true,
    dismissLabel: "Dismiss message",
    onDismiss: () =>
      dismissNotification(`${ticket.ticket_id}-${uniqueIDAnchor}`),
    content: content,
    loading: loading,
  };
};
